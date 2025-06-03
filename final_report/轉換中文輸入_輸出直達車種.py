import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# 輸入可將中文車站轉換為站牌ID的CSV檔案路徑
csv_path = r"C:\Users\USER\Desktop\cycu_oop_11372004\final_report\all_bus_stops_by_route.csv"
stop_df = pd.read_csv(csv_path)[["站名", "站牌ID"]].drop_duplicates()

def get_stop_ids_by_name(name: str) -> list:
    matches = stop_df[stop_df["站名"].str.contains(name.strip(), case=False, na=False)]
    if matches.empty:
        print(f"查無「{name}」相關站牌")
        return []
    return matches["站牌ID"].tolist()

async def fetch_bus_routes_by_stop_id(stop_id: str) -> set:
    url = f"https://ebus.gov.taipei/Stop/RoutesOfStop?Stopid={stop_id}"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(3000)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("div#ResultList ul.auto-list-pool li")
    routes = {
        item.select_one("p.auto-list-routelist-bus").get_text(strip=True)
        for item in items if item.select_one("p.auto-list-routelist-bus")
    }
    return routes

async def fetch_all_routes_by_stop_ids(stop_ids: list) -> set:
    all_routes = set()
    for stop_id in stop_ids:
        routes = await fetch_bus_routes_by_stop_id(stop_id)
        all_routes.update(routes)
    return all_routes

async def check_direct_bus_from_names():
    stop1 = input("請輸入出發站（中文名稱）：").strip()
    stop2 = input("請輸入目的站（中文名稱）：").strip()

    ids1 = get_stop_ids_by_name(stop1)
    ids2 = get_stop_ids_by_name(stop2)

    if not ids1 or not ids2:
        print("無法比對，請確認站名正確")
        return

    print(f"\n正在查詢「{stop1}」的所有路線...")
    routes1 = await fetch_all_routes_by_stop_ids(ids1)

    print(f"正在查詢「{stop2}」的所有路線...")
    routes2 = await fetch_all_routes_by_stop_ids(ids2)

    direct = routes1 & routes2
    if direct:
        print(f"\n可直達的公車路線如下：")
        for route in sorted(direct):
            print(f"{route}")
    else:
        print("\n無直達公車，需轉乘")

if __name__ == "__main__":
    asyncio.run(check_direct_bus_from_names())