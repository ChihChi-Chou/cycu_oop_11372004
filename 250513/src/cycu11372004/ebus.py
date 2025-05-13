import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


async def get_bus_info_go(bus_id):
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={bus_id}"
    
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
            inputs = li.select("input")

            if not inputs or len(inputs) == 0:
                print(f"第 {idx} 筆資料缺少必要的 input 元素，跳過。")
                continue

            stop_id = inputs[0].get('value', '未知站牌ID')
            all_stations.append(stop_id)

        except Exception as e:
            print(f"第 {idx} 筆資料處理錯誤：{e}")

    if not all_stations:
        print("沒有成功抓取到任何站牌資訊。")
        return

    print("\n抓到的站牌資訊如下：")
    print(all_stations)


# 執行主程式
if __name__ == "__main__":
    bus_id = input("請告訴我公車代碼：").strip()
    asyncio.run(get_bus_info_go(bus_id))