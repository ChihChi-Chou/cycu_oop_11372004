import asyncio
import csv
import os
import folium
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CSV_PATH = r"C:\Users\USER\Desktop\cycu_oop_11372004\250527\all_bus_stops_by_route.csv"
ROUTE_MAP_CSV = r"C:\Users\USER\Desktop\cycu_oop_11372004\final_report\taipei_bus_routes.csv"

def get_stop_id_by_direction_and_name(direction, stop_name):
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["方向"].strip() == direction and row["站名"].strip() == stop_name:
                return row["站牌ID"].strip()
    return None

def load_route_mapping(csv_path):
    mapping = {}
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["路線名稱"].strip()
            code = row["公車代碼"].strip()
            mapping[name] = code
    return mapping

async def fetch_bus_routes(station_id):
    url = f"https://ebus.gov.taipei/Stop/RoutesOfStop?Stopid={station_id}"
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        await browser.close()
    soup = BeautifulSoup(html, "html.parser")
    bus_items = soup.select("div#ResultList ul.auto-list-pool li")
    bus_routes = []
    for li in bus_items:
        try:
            bus_number = li.select_one("p.auto-list-routelist-bus").get_text(strip=True)
            bus_routes.append(bus_number)
        except Exception as e:
            print(f"抓取公車路線時發生錯誤：{e}")
    return set(bus_routes)

async def get_bus_route_stops(route_id: str) -> dict:
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id.strip()}"
    result = {"去程": [], "返程": []}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector("div#GoDirectionRoute li, div#BackDirectionRoute li", timeout=10000)
        except:
            print("無法載入公車站牌頁面，請確認路線代碼是否正確。")
            return result

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")

    for direction, selector in [("去程", "div#GoDirectionRoute li"), ("返程", "div#BackDirectionRoute li")]:
        station_items = soup.select(selector)
        for idx, li in enumerate(station_items, start=1):
            spans = li.select("span.auto-list-stationlist span")
            inputs = li.select("input")
            if len(spans) >= 3 and len(inputs) >= 3:
                result[direction].append({
                    "順序": idx,
                    "站名": spans[2].get_text(strip=True),
                    "站牌ID": inputs[0]['value'],
                    "lat": float(inputs[1]['value']),
                    "lon": float(inputs[2]['value'])})
    return result

def plot_full_map_with_stations(route_id, route_data, start_info, dest_info, direction, output_path):
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    color = "red" if direction == "去程" else "blue"
    stops = route_data.get(direction, [])

    # 找起訖站的 index
    try:
        idx_start = next(i for i, stop in enumerate(stops) if stop["站名"] == start_info["站名"])
        idx_end = next(i for i, stop in enumerate(stops) if stop["站名"] == dest_info["站名"])
    except StopIteration:
        print("⚠️ 無法在路線中找到起點或終點站，無法繪製地圖。")
        return

    # 取得從起點到終點的子序列
    if idx_start <= idx_end:
        segment_stops = stops[idx_start:idx_end + 1]
    else:
        segment_stops = stops[idx_end:idx_start + 1][::-1]

    # 畫站牌
    for i, stop in enumerate(segment_stops, start=1):
        folium.CircleMarker(
            location=[stop["lat"], stop["lon"]],
            radius=12,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_child(folium.Popup(f'{direction}：{stop["站名"]}')).add_to(m)

        folium.map.Marker(
            [stop["lat"], stop["lon"]],
            icon=folium.DivIcon(html=f"""<div style="font-size:10pt; color:white;
                background:{color}; border-radius:50%; width:18px; height:18px;
                text-align:center; line-height:18px;">{i}</div>""")
        ).add_to(m)

    # 起訖點標註
    folium.Marker(
        location=[start_info['lat'], start_info['lon']],
        popup=f"起點站：{start_info['站名']}",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        location=[dest_info['lat'], dest_info['lon']],
        popup=f"終點站：{dest_info['站名']}",
        icon=folium.Icon(color="orange", icon="flag")
    ).add_to(m)

    m.save(output_path)
    return output_path

async def find_direct_bus():
    direction = input("請輸入查詢方向（去程/返程）：").strip()
    if direction not in ("去程", "返程"):
        print("方向輸入錯誤，請輸入「去程」或「返程」")
        return

    start_name = input("請輸入所在車站名稱：").strip()
    dest_name = input("請輸入目的地車站名稱：").strip()

    start_id = get_stop_id_by_direction_and_name(direction, start_name)
    dest_id = get_stop_id_by_direction_and_name(direction, dest_name)

    if not start_id or not dest_id:
        print("站名或方向輸入錯誤，請確認站名與方向是否正確。")
        return

    print(f"所在車站ID: {start_id}, 目的地車站ID: {dest_id}")

    print("正在抓取所在車站的公車路線...")
    routes_1 = await fetch_bus_routes(start_id)
    print("正在抓取目的地車站的公車路線...")
    routes_2 = await fetch_bus_routes(dest_id)

    common_routes = routes_1.intersection(routes_2)
    route_map = load_route_mapping(ROUTE_MAP_CSV)

    if common_routes:
        print("\n以下公車可以直達兩站：")
        for route in sorted(common_routes):
            route_code = route_map.get(route, "（查無代碼）")
            print(f"{route} → 公車代碼：{route_code}")

        if input("\n是否繪製直達路線圖？（y/n）：").strip().lower() == "y":
            for route in common_routes:
                print(f"\n正在處理路線：{route} ...")
                route_id = route_map.get(route)
                if not route_id or not route_id.isdigit():
                    print(f"⚠️ 無法取得路線代碼：{route}")
                    continue

                route_data = await get_bus_route_stops(route_id)
                stops = route_data.get(direction, [])
                start_info = next((s for s in stops if s["站名"] == start_name), None)
                dest_info = next((s for s in stops if s["站名"] == dest_name), None)

                if not start_info or not dest_info:
                    print(f"⚠️ 無法在{direction}中找到起點或終點，略過此路線。")
                    continue

                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                map_file = os.path.join(desktop, f"直達公車_{route}_{direction}_區段.html")

                plot_full_map_with_stations(route_id, route_data, start_info, dest_info, direction, map_file)
                print(f"✅ 地圖已儲存至：{map_file}")
    else:
        print("\n沒有公車可以直達兩站。")

if __name__ == "__main__":
    asyncio.run(find_direct_bus())
