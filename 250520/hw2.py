import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取 midterm_scores.csv 檔案
file_path = r"C:\Users\User\Desktop\cycu_oop_11372004\250520\midterm_scores.csv"

try:
    # 使用 pandas 讀取 CSV 檔案
    data = pd.read_csv(file_path)
    
    # 定義科目及顏色
    subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'darkblue', 'purple']
    
    # 設定分數區間
    bins = np.arange(0, 101, 10)  # 分數區間 0-10, 11-20, ..., 91-100
    bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
    x = np.arange(len(bin_labels))  # X 軸位置
    
    # 繪製長條圖
    plt.figure(figsize=(14, 8))
    bar_width = 0.1  # 每個長條的寬度
    for i, (subject, color) in enumerate(zip(subjects, colors)):
        # 計算每個分數區間的人數
        counts, _ = np.histogram(data[subject], bins=bins)
        # 偏移每個科目的位置
        plt.bar(x + i * bar_width, counts, width=bar_width, color=color, label=subject)
    
    # 圖表設定
    plt.title("Score Range", fontsize=16)
    plt.xlabel("Distribution of Scores", fontsize=14)
    plt.ylabel("Number of Students", fontsize=14)
    plt.xticks(x + (len(subjects) - 1) * bar_width / 2, bin_labels, rotation=45)
    plt.legend(title="Subjects", fontsize=12)
    plt.tight_layout()
    
    # 顯示圖表
    plt.show()

except FileNotFoundError:
    print(f"檔案未找到：{file_path}")
except Exception as e:
    print(f"讀取檔案時發生錯誤：{e}")