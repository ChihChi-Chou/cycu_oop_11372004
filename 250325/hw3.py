import requests
from bs4 import BeautifulSoup

def get_bus_arrival(stop_name_or_number):
    """
    查詢忠孝幹線公車到站時間 (去程)
    :param stop_name_or_number: 公車站名稱或站牌號碼
    :return: 到站時間資訊或錯誤訊息
    """
    url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.encoding = 'utf-8'

        # 檢查請求是否成功
        if response.status_code != 200:
            return f"錯誤：無法連接到網站，狀態碼 {response.status_code}"

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到去程區塊
        direction_block = soup.find('div', id='go')
        if not direction_block:
            return "錯誤：無法找到去程區塊，請確認網站結構是否正確"

        # 找到所有站點資訊
        stops = direction_block.find_all('div', class_='stop')

        # 遍歷站點，查找目標站名或站牌號碼
        for stop in stops:
            stop_title = stop.find('div', class_='stopTitle').text.strip()
            stop_number = stop.find('div', class_='stopID').text.strip()  # 假設站牌號碼在 stopID 標籤中
            if stop_name_or_number in stop_title or stop_name_or_number == stop_number:
                # 提取到站時間資訊
                arrival_info = stop.find('div', class_='arrival').text.strip()
                if "分" in arrival_info:
                    return f"公車忠孝幹線，{stop_title} 預計 {arrival_info} 到站"
                elif "進站" in arrival_info:
                    return f"公車忠孝幹線，{stop_title} 公車已進站"

        # 如果站名或站牌號碼不在路線中
        return f"錯誤：{stop_name_or_number} 不在忠孝幹線的路線內"

    except Exception as e:
        return f"錯誤：{str(e)}"

# 主程式
if __name__ == "__main__":
    stop_name_or_number = input("請輸入公車站名稱或站牌號碼：")
    result = get_bus_arrival(stop_name_or_number)
    print(result)