import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定 Matplotlib 使用支援中文字的字型
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 使用微軟正黑體

def read_and_plot_csv(file_path):
    # 讀取 CSV 檔案，跳過第一列資料，並指定 UTF-8 編碼
    df = pd.read_csv(file_path, skiprows=1, header=None, encoding='utf-8')
    
    # 假設第一行為日期，第四行為 y1，十四行為 y2
    x = pd.to_datetime(df.iloc[:, 0], format='%Y%m%d')  # 將日期轉換為 datetime 格式
    y1 = df.iloc[:, 3]  # 第四行數列
    y2 = df.iloc[:, 13]  # 第十四行數列

    # 按日期排序
    sorted_indices = x.argsort()
    x = x.iloc[sorted_indices]
    y1 = y1.iloc[sorted_indices]
    y2 = y2.iloc[sorted_indices]

    # 繪製圖表
    plt.figure(figsize=(10, 6))
    plt.plot(x, y1, label='本行買入', color='red')
    plt.plot(x, y2, label='本行賣出', color='blue')
    plt.xlabel('日期')  # 中文標籤
    plt.ylabel('數值')  # 中文標籤
    plt.title('美金匯率走勢')  # 中文標題
    plt.ylim(32, 33.4)  # 設定 y 軸範圍
    plt.legend()
    plt.xticks(rotation=45)  # 日期旋轉以便顯示
    plt.tight_layout()
    plt.show()

# 使用範例
file_path = '0325.csv'
read_and_plot_csv(file_path)