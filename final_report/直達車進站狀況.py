import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import csv
import os
import folium

CSV_PATH = r"C:\Users\User\Desktop\cycu_oop_11372004\final_report\all_bus_stops_by_route.csv"
ROUTE_MAP_CSV = r"C:\Users\User\Desktop\cycu_oop_11372004\final_report\taipei_bus_routes.csv"

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
            await page.wait_for_selector("div#GoDirectionRoute li, div#BackDirectionRoute li", timeout=50000)
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

            # 判斷即時時間欄位，去程通常 spans[0] 是即時時間，返程如果抓不到用 fallback
            arrival_time = "無資料"
            try:
                if direction == "去程":
                    arrival_time = spans[0].get_text(strip=True)
                elif direction == "返程":
                    arrival_time = spans[0].get_text(strip=True)
                    if not arrival_time:
                        arrival_time = spans[1].get_text(strip=True) if len(spans) > 1 else "無資料"
            except Exception:
                pass

            if len(spans) >= 3 and len(inputs) >= 3:
                result[direction].append({
                    "順序": idx,
                    "站名": spans[2].get_text(strip=True),
                    "站牌ID": inputs[0]['value'],
                    "lat": float(inputs[1]['value']),
                    "lon": float(inputs[2]['value']),
                    "到站時間": arrival_time
                })
    return result

def plot_combined_segment_map(route_id, route_data, start_name, dest_name, output_path):
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)
    segment_color = "orange"

    valid_direction = None
    all_stops = []

    for direction in ["去程", "返程"]:
        stops = route_data.get(direction, [])
        try:
            idx_start = next(i for i, stop in enumerate(stops) if stop["站名"] == start_name)
            idx_end = next(i for i, stop in enumerate(stops) if stop["站名"] == dest_name)
            if idx_start <= idx_end:
                valid_direction = direction
                all_stops = stops
                break
        except StopIteration:
            continue

    if not valid_direction:
        print("⚠️ 無法在任一方向中找到符合順序的起點與終點，無法繪圖。")
        return

    coords_all = []
    for i, stop in enumerate(all_stops, start=1):
        coords_all.append((stop["lat"], stop["lon"]))
        folium.CircleMarker(
            location=(stop["lat"], stop["lon"]),
            radius=8,
            color=segment_color,
            fill=True,
            fill_color=segment_color,
            fill_opacity=0.7
        ).add_child(folium.Popup(f'{valid_direction}：{stop["站名"]}\n即時到站時間：{stop.get("到站時間", "無資料")}')).add_to(m)

        folium.map.Marker(
            [stop["lat"], stop["lon"]],
            icon=folium.DivIcon(html=f"""<div style="font-size:10pt; color:white;
                background:{segment_color}; border-radius:50%; width:18px; height:18px;
                text-align:center; line-height:18px;">{i}</div>""")
        ).add_to(m)

    folium.PolyLine(coords_all, color=segment_color, weight=4, opacity=0.9).add_to(m)

    for stop in all_stops:
        if stop["站名"] == start_name:
            folium.Marker(
                location=[stop['lat'], stop['lon']],
                popup=f"起點站：{stop['站名']}\n即時到站時間：{stop.get('到站時間', '無資料')}",
                icon=folium.Icon(color="green", icon="play")
            ).add_to(m)
        if stop["站名"] == dest_name:
            folium.Marker(
                location=[stop['lat'], stop['lon']],
                popup=f"終點站：{stop['站名']}\n即時到站時間：{stop.get('到站時間', '無資料')}",
                icon=folium.Icon(color="darkred", icon="flag")
            ).add_to(m)

    m.save(output_path)
    return output_path

async def find_direct_bus_with_arrival_time_and_map():
    print("📍 請選擇出發與目的地站牌：\n")
    start_name, start_id = choose_stop_id("出發地")
    if not start_id:
        return
    dest_name, dest_id = choose_stop_id("目的地")
    if not dest_id:
        return

    print(f"\n出發地站牌ID: {start_id}，目的地站牌ID: {dest_id}")

    print("\n正在查詢公車路線...")
    routes_start = await fetch_bus_routes(start_id)
    routes_dest = await fetch_bus_routes(dest_id)

    common_routes = routes_start.intersection(routes_dest)
    route_map = load_route_mapping(ROUTE_MAP_CSV)

    if not common_routes:
        print("\n❌ 無公車可直達兩站。")
        return

    print("\n✅ 以下公車可直達兩站：")
    for route_name in sorted(common_routes):
        route_code = route_map.get(route_name, None)
        if not route_code or not route_code.isdigit():
            print(f"{route_name} → （無法取得有效代碼，無法查詢到站時間）")
            continue

        route_stops = await get_bus_route_stops(route_code)

        valid_direction = None
        for direction in ["去程", "返程"]:
            stops = route_stops.get(direction, [])
            try:
                idx_start = next(i for i, stop in enumerate(stops) if stop["站名"] == start_name)
                idx_dest = next(i for i, stop in enumerate(stops) if stop["站名"] == dest_name)
                if idx_start < idx_dest:
                    if all(stop.get("到站時間", "") in ("", "無資料") for stop in stops):
                        continue
                    valid_direction = direction
                    break
            except StopIteration:
                continue

        if not valid_direction:
            print(f"{route_name}（代碼 {route_code}）→ 無法找到先到出發地再到目的地且有即時資料的方向，跳過此路線。")
            continue

        filtered_stops = route_stops[valid_direction]

        print(f"{route_name}（代碼 {route_code}）→ {valid_direction} 各站即將到站時間：")
        for stop in filtered_stops:
            arrival = stop.get("到站時間", "無資料")
            print(f"  {stop['順序']}. {stop['站名']} → {arrival}")

        print(f"🗺️ 正在繪製路線圖 {route_name} ...")
        map_file = os.path.join(os.path.expanduser("~"), "Desktop", f"直達公車_{route_name}_{valid_direction}_區段圖.html")
        plot_combined_segment_map(route_code, {valid_direction: filtered_stops}, start_name, dest_name, map_file)
        print(f"✅ 地圖已儲存至：{map_file}")

if __name__ == "__main__":
    asyncio.run(find_direct_bus_with_arrival_time_and_map())
