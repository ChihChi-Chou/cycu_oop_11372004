import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def find_bus_status():
    station_id = input("請告訴我站牌代碼：").strip()
    url = f"https://ebus.gov.taipei/Stop/RoutesOfStop?Stopid={station_id}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        html = await page.content()
        await browser.close()

    soup = BeautifulSoup(html, "html.parser")

    # 尋找所有公車進站狀況
    bus_items = soup.select("div#ResultList ul.auto-list-pool li")

    all_buses = []

    for idx, li in enumerate(bus_items, start=1):
        try:
            # 抓取公車號碼
            bus_number = li.select_one("p.auto-list-routelist-bus").get_text(strip=True)
            # 抓取公車方向與目的地
            bus_destination = li.select_one("p.auto-list-routelist-place").get_text(strip=True)
            # 抓取進站狀況
            bus_status = li.select_one("span.auto-list-routelist-position").get_text(strip=True)

            # 將資料以逗號分隔的格式存入陣列
            bus_info = f"{bus_number},{bus_destination},{bus_status}"
            all_buses.append(bus_info)
        except Exception as e:
            print(f"第 {idx} 筆資料處理錯誤：{e}")

    print("\n抓到的公車進站狀況：\n")
    for bus in all_buses:
        print(bus)

# 執行函數
if __name__ == "__main__":
    asyncio.run(find_bus_status())