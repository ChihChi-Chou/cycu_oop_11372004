import pandas as pd

# 讀取 midterm_scores.csv 檔案
file_path = r"C:\Users\User\Desktop\cycu_oop_11372004\250520\midterm_scores.csv"

try:
    # 使用 pandas 讀取 CSV 檔案
    data = pd.read_csv(file_path)
    
    # 計算每位學生低於 60 分的科目數量
    subjects = ['Chinese', 'English', 'Math', 'History', 'Geography', 'Physics', 'Chemistry']
    data['Fail_Count'] = (data[subjects] < 60).sum(axis=1)
    
    # 篩選出低於 60 分的科目超過半數（4 科以上）的學生
    filtered_students = data[data['Fail_Count'] > 3]
    
    # 列出姓名、學號及各科成績
    result = filtered_students[['Name', 'StudentID'] + subjects]
    print("以下是低於 60 分科目超過半數的學生：")
    print(result)

    # 輸入儲存路徑
    output_path = input("請輸入輸出檔案的完整路徑（包含檔名，例如 output.csv）：")
    
    # 將結果輸出為 CSV 檔案
    result.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"結果已輸出至：{output_path}")
    
except FileNotFoundError:
    print(f"檔案未找到：{file_path}")
except Exception as e:
    print(f"讀取檔案時發生錯誤：{e}")