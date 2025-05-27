import asyncio
import os
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import folium

async def fetch_bus_routes(station_id):
    """
    抓取指定站牌的所有公車路線
    """
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
    """
    抓取公車路線的站牌資訊
    """
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

def plot_route_map_with_stops(route_data: dict, station_1: dict, station_2: dict, output_path: str):
    """
    繪製地圖，標註兩車站及直達車路線，並繪製公車路線
    """
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)

    # 標註兩車站
    for station, color in [(station_1, "green"), (station_2, "red")]:
        folium.Marker(
            location=[station["lat"], station["lon"]],
            popup=f'{station["站名"]} (ID: {station["站牌ID"]})',
            icon=folium.Icon(color=color)
        ).add_to(m)

    # 繪製直達車路線
    for direction, color in zip(["去程", "返程"], ["red", "blue"]):
        stops = route_data.get(direction, [])
        if not stops:
            continue

        # 繪製路線線條
        polyline = [(stop["lat"], stop["lon"]) for stop in stops]
        folium.PolyLine(
            locations=polyline,
            color=color,
            weight=5,
            opacity=0.7
        ).add_to(m)

        # 標註每個站牌
        for stop in stops:
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
                    text-align:center; line-height:18px;">{stop["順序"]}</div>""")
            ).add_to(m)

    # 儲存地圖
    m.save(output_path)
    return output_path

async def main():
    station_id_1 = input("請輸入所在車站的站牌代碼：").strip()
    station_id_2 = input("請輸入目的地車站的站牌代碼：").strip()

    print("正在抓取第一個站牌的公車路線...")
    routes_1 = await fetch_bus_routes(station_id_1)
    print("正在抓取第二個站牌的公車路線...")
    routes_2 = await fetch_bus_routes(station_id_2)

    common_routes = routes_1.intersection(routes_2)

    if not common_routes:
        print("\n沒有公車可以直達兩站。")
        return

    print("\n以下公車可以直達兩站：")
    for route in common_routes:
        print(route)

    # 抓取直達車的站牌資訊
    route_id = list(common_routes)[0]  # 假設只繪製第一條直達車路線
    print(f"\n正在抓取公車路線 {route_id} 的站牌資料...")
    route_data = await get_bus_route_stops(route_id)

    # 模擬兩車站的地理資訊（實際應從 API 獲取）
    station_1 = {"站名": "站牌1", "站牌ID": station_id_1, "lat": 25.0330, "lon": 121.5654}
    station_2 = {"站名": "站牌2", "站牌ID": station_id_2, "lat": 25.0370, "lon": 121.5630}

    # 詢問儲存路徑
    user_path = input("\n請輸入輸出 HTML 地圖完整檔名（可留空使用桌面）：").strip()
    if not user_path:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        user_path = os.path.join(desktop, f"direct_bus_route_{route_id}.html")

    print("\n正在建立地圖並標註站牌...")
    output_map_path = plot_route_map_with_stops(route_data, station_1, station_2, user_path)

    print(f"\n地圖已儲存至：{output_map_path}")

if __name__ == "__main__":
    asyncio.run(main())