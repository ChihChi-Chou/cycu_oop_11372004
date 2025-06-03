import asyncio
import csv
import os
import folium
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

CSV_PATH = r"C:\Users\USER\Desktop\cycu_oop_11372004\250527\all_bus_stops_by_route.csv"
ROUTE_MAP_CSV = r"C:\Users\USER\Desktop\cycu_oop_11372004\final_report\taipei_bus_routes.csv"

def list_stop_options_by_name(stop_name):
    unique_ids = set()
    options = []
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["站名"].strip() == stop_name:
                stop_id = row["站牌ID"].strip()
                if stop_id not in unique_ids:
                    unique_ids.add(stop_id)
                    options.append({"站牌ID": stop_id})
    return options

def choose_stop_id(stop_label):
    stop_name = input(f"請輸入{stop_label}站名：").strip()
    options = list_stop_options_by_name(stop_name)
    if not options:
        print(f"❌ 找不到站名「{stop_name}」的資料。")
        return None, None

    print(f"\n找到以下「{stop_name}」的站牌ID：")
    for idx, opt in enumerate(options, 1):
        print(f"{idx}. 站牌ID：{opt['站牌ID']}")

    while True:
        try:
            choice = int(input(f"請選擇{stop_label}對應站牌ID（輸入編號）：").strip())
            if 1 <= choice <= len(options):
                return stop_name, options[choice - 1]["站牌ID"]
            else:
                print("⚠️ 超出選項範圍，請重新輸入。")
        except ValueError:
            print("⚠️ 請輸入有效的編號。")

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
    return {li.select_one("p.auto-list-routelist-bus").get_text(strip=True) for li in bus_items}

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

def plot_combined_segment_map(route_id, route_data, start_name, dest_name, output_path):
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    color_map = {"去程": "red", "返程": "blue"}

    for direction in ["去程", "返程"]:
        stops = route_data.get(direction, [])
        color = color_map[direction]

        try:
            idx_start = next(i for i, stop in enumerate(stops) if stop["站名"] == start_name)
            idx_end = next(i for i, stop in enumerate(stops) if stop["站名"] == dest_name)
        except StopIteration:
            print(f"⚠️ 無法在 {direction} 中找到起點或終點，略過此方向。")
            continue

        segment = stops[idx_start:idx_end + 1] if idx_start <= idx_end else stops[idx_end:idx_start + 1][::-1]

        coords = []
        for i, stop in enumerate(segment, start=1):
            coords.append((stop["lat"], stop["lon"]))
            folium.CircleMarker(
                location=[stop["lat"], stop["lon"]],
                radius=10,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6
            ).add_child(folium.Popup(f'{direction}：{stop["站名"]}')).add_to(m)

            folium.map.Marker(
                [stop["lat"], stop["lon"]],
                icon=folium.DivIcon(html=f"""<div style="font-size:10pt; color:white;
                    background:{color}; border-radius:50%; width:18px; height:18px;
                    text-align:center; line-height:18px;">{i}</div>""")
            ).add_to(m)

        folium.PolyLine(coords, color=color, weight=4, opacity=0.7).add_to(m)

    # 起訖點
    for stops in route_data.values():
        for stop in stops:
            if stop["站名"] == start_name:
                folium.Marker(
                    location=[stop['lat'], stop['lon']],
                    popup=f"起點站：{stop['站名']}",
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)
            if stop["站名"] == dest_name:
                folium.Marker(
                    location=[stop['lat'], stop['lon']],
                    popup=f"終點站：{stop['站名']}",
                    icon=folium.Icon(color="orange", icon="flag")
                ).add_to(m)

    m.save(output_path)
    return output_path

async def find_direct_bus():
    print("📍 請選擇出發與目的地站牌：\n")
    start_name, start_id = choose_stop_id("出發地")
    if not start_id:
        return
    dest_name, dest_id = choose_stop_id("目的地")
    if not dest_id:
        return

    print(f"\n出發地站牌ID: {start_id}，目的地站牌ID: {dest_id}")

    print("\n正在查詢公車路線...")
    routes_1 = await fetch_bus_routes(start_id)
    routes_2 = await fetch_bus_routes(dest_id)

    common_routes = routes_1.intersection(routes_2)
    route_map = load_route_mapping(ROUTE_MAP_CSV)

    if common_routes:
        print("\n✅ 以下公車可直達兩站：")
        for route in sorted(common_routes):
            route_code = route_map.get(route, "（查無代碼）")
            print(f"{route} → 公車代碼：{route_code}")

        if input("\n是否繪製雙向路線段圖？（y/n）：").strip().lower() == "y":
            for route in common_routes:
                print(f"\n🚌 正在處理路線：{route} ...")
                route_id = route_map.get(route)
                if not route_id or not route_id.isdigit():
                    print(f"⚠️ 無法取得路線代碼：{route}")
                    continue

                route_data = await get_bus_route_stops(route_id)
                map_file = os.path.join(os.path.expanduser("~"), "Desktop", f"直達公車_{route}_雙向區段圖.html")
                plot_combined_segment_map(route_id, route_data, start_name, dest_name, map_file)
                print(f"✅ 地圖已儲存至：{map_file}")
    else:
        print("\n❌ 無公車可直達兩站。")

if __name__ == "__main__":
    asyncio.run(find_direct_bus())
