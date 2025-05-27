import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def find_bus_and_plot(route_id: str):
    """
    抓取公車站點資訊，並將路線繪製於地圖上。
    """
    route_id = route_id.strip()
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        try:
            await page.wait_for_selector("div#GoDirectionRoute li", timeout=10000)
        except:
            print("網頁載入超時，請確認公車代碼是否正確。")
            return

        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")
    station_items = soup.select("div#GoDirectionRoute li")

    if not station_items:
        print("未找到任何站牌資料，請確認公車代碼是否正確。")
        return

    all_stations = []

    for idx, li in enumerate(station_items, start=1):
        try:
            spans = li.select("span.auto-list-stationlist span")
            inputs = li.select("input")

            stop_time = spans[0].get_text(strip=True)
            stop_number = spans[1].get_text(strip=True)
            stop_name = spans[2].get_text(strip=True)

            stop_id = inputs[0]['value']
            latitude = float(inputs[1]['value'])
            longitude = float(inputs[2]['value'])

            station = [stop_time, stop_number, stop_name, stop_id, latitude, longitude]
            all_stations.append(station)

        except Exception as e:
            print(f"第 {idx} 筆資料處理錯誤：{e}")

    if not all_stations:
        print("沒有成功抓取到任何站牌資訊。")
        return

    # 輸出所有站名
    print("\n抓到的站牌資訊如下：")
    for station in all_stations:
        print(f"站名: {station[2]}")

    # 生成 GeoDataFrame
    line_coords = [(station[5], station[4]) for station in all_stations]  # 經緯度順序為 (lon, lat)
    bus_route = gpd.GeoDataFrame(geometry=[LineString(line_coords)], crs="EPSG:4326")
    bus_stops = gpd.GeoDataFrame(geometry=[Point(coord) for coord in line_coords], crs="EPSG:4326")

    # 讀取地理資料檔案，指定圖層
    file_path = r"C:\Users\User\Desktop\cycu_oop_11372004\250520\OFiles_9e222fea-bafb-4436-9b17-10921abc6ef2"
    gdf = gpd.read_file(file_path, layer='TOWN_MOI_1140318')  # 指定圖層

    # 篩選基隆、台北、新北、桃園市內所有鄉鎮區
    cities = ["基隆市", "臺北市", "新北市", "桃園市"]
    filtered_gdf = gdf[gdf["COUNTYNAME"].isin(cities)]

    # 移除無效的幾何形狀
    filtered_gdf = filtered_gdf[filtered_gdf.geometry.is_valid]
    filtered_gdf = filtered_gdf.dropna(subset=['geometry'])

    # 繪製地圖
    fig, ax = plt.subplots(figsize=(12, 12))
    filtered_gdf.plot(ax=ax, color="lightgray", edgecolor="black")  # 灰色填充，黑色邊界
    bus_route.plot(ax=ax, color="red", linewidth=2)  # 公車路線

    # 移除圖表標題、橫縱軸及圖例
    ax.set_title("")
    ax.set_axis_off()
    ax.legend()

    # 顯示地圖
    plt.show()

# 執行主程式
if __name__ == "__main__":
    route_id = input("請輸入巴士路線 ID: ").strip()
    asyncio.run(find_bus_and_plot(route_id))