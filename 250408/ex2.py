from datetime import datetime

def calculate_julian_date():
    # 設定 Julian date 起始點 (公元前 4713 年 1 月 1 日中午)
    julian_start_days = 1721425.5  # Julian 起始點的天數 (以西元 1 年為基準)

    # 計算西元 1 年的太陽日
    print(f"西元 1 年 1 月 1 日的太陽日 (Julian date) 為：{julian_start_days:.6f}")

    # 使用者輸入日期與時間
    year = int(input("請輸入西元年 (YYYY，若為西元前請輸入負數)："))
    month = int(input("請輸入西元月 (MM)："))
    day = int(input("請輸入西元日 (DD)："))
    hour = int(input("請輸入小時 (HH)："))
    minute = int(input("請輸入分鐘 (MM)："))

    # 處理西元前的年份
    if year < 0:
        year += 1  # 西元前的年份處理，因為沒有西元 0 年

    # 計算 Julian Date
    if month <= 2:
        year -= 1
        month += 12

    # Julian Day Number (JDN) 計算公式
    A = year // 100
    B = 2 - A + (A // 4)
    JDN = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5

    # 加上當天的時間 (小數部分)
    fractional_day = (hour + minute / 60) / 24
    julian_date = JDN + fractional_day

    # 格式化輸出日期與時間
    formatted_time = f"{abs(year):04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
    if year < 0:
        formatted_time = f"西元前 {formatted_time}"
    print(f"輸入的日期與時間為：{formatted_time}")

     # 計算該天是星期幾（中文）
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_index = int(JDN + 1) % 7  # Julian Day Number 的星期計算公式
    weekday = weekdays[weekday_index]
    print(f"輸入的日期是：{weekday}")


    # 輸出太陽日
    print(f"該時刻的太陽日 (Julian date) 為：{julian_date:.6f}")

# 呼叫函數
calculate_julian_date()