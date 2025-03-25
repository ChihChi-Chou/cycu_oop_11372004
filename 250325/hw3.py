from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def get_bus_arrival_with_selenium(stop_name):
    """
    使用 Selenium 查詢忠孝幹線公車到站時間 (去程)
    :param stop_name: 公車站名稱
    :return: 到站時間資訊或錯誤訊息
    """
    # 使用 Selenium 打開瀏覽器
    driver = webdriver.Chrome()  # 確保已安裝 ChromeDriver
    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"
    driver.get(url)

    # 等待去程區塊加載
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'go'))
        )
    except:
        driver.quit()
        return "錯誤：去程區塊未加載，請確認網站結構或網路狀態"

    # 獲取頁面 HTML
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 找到去程區塊
    direction_block = soup.find('div', id='go')  # 去程區塊

    # 檢查是否找到去程區塊
    if direction_block is None:
        driver.quit()
        return "錯誤：無法找到去程區塊，請確認網站結構是否正確"

    # 找到所有站點資訊
    stops = direction_block.find_all('div', class_='stop')

    # 遍歷站點，查找目標站名
    for stop in stops:
        stop_title = stop.find('div', class_='stopTitle').text.strip()
        if stop_name in stop_title:
            # 提取到站時間資訊
            arrival_info = stop.find('div', class_='arrival').text.strip()
            driver.quit()
            if "分" in arrival_info:
                return f"公車忠孝幹線，{stop_name} 預計 {arrival_info} 到站"
            elif "進站" in arrival_info:
                return f"公車忠孝幹線，{stop_name} 公車已進站"

    # 如果站名不在路線中
    driver.quit()
    return f"錯誤：{stop_name} 不在忠孝幹線的路線內"

# 使用範例
stop_name = input("請輸入公車站名稱：")
result = get_bus_arrival_with_selenium(stop_name)
print(result)