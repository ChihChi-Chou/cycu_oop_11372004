import pandas as pd

def read_and_sum_excel(file_path):
    # 讀取 Excel 檔案
    df = pd.read_excel(file_path)
    
    # 假設第一欄為 'x'，第二欄為 'y'
    df['sum'] = df.iloc[:, 0] + df.iloc[:, 1]
    
    # 輸出結果
    print(df)

# 使用範例
file_path = '311.xlsx'
read_and_sum_excel(file_path)