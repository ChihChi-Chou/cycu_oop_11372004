import requests
import html
import pandas as pd
from bs4 import BeautifulSoup

url = '''https://pda5284.gov.taipei/MQS/route.jsp?rid=10417'''

# 發送 GET 請求
response = requests.get(url)

# 確保請求成功
if response.status_code == 200:
    # 將內容寫入 bus1.html
    with open("bus1.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("網頁已成功下載並儲存為 bus1.html")

    # 重新讀取並解碼 HTML
    with open("bus1.html", "r", encoding="utf-8") as file:
        content = file.read()
        decoded_content = html.unescape(content)  # 解碼 HTML 實體
        print(decoded_content)  # 顯示解碼後的內容

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(content, "html.parser")

    # 找到所有表格
    tables = soup.find_all("table")

    # 初始化 DataFrame 列表
    df_go = None
    df_back = None

    # 遍歷表格
    for table in tables:
        # 處理去程資料
        rows_go = []
        for tr in table.find_all("tr", class_=["ttego1", "ttego2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
                stop_link = td.find("a")["href"] if td.find("a") else None
                rows_go.append({"站點名稱": stop_name, "連結": stop_link})
        if rows_go:
            df_go = pd.DataFrame(rows_go)

        # 處理返程資料
        rows_back = []
        for tr in table.find_all("tr", class_=["tteback1", "tteback2"]):
            td = tr.find("td")
            if td:
                stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
                stop_link = td.find("a")["href"] if td.find("a") else None
                rows_back.append({"站點名稱": stop_name, "連結": stop_link})
        if rows_back:
            df_back = pd.DataFrame(rows_back)

    # 輸出結果
    if df_go is not None:
        print("去程(往松山車站):")
        print(df_go)
    else:
        print("未找到去程資料。")

    if df_back is not None:
        print("返程(往蘆洲):")
        print(df_back)
    else:
        print("未找到返程資料。")
else:
    print(f"無法下載網頁，HTTP 狀態碼: {response.status_code}")