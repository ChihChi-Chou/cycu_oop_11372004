import asyncio
from bus_info_11372009 import find_bus  # 匯入 bus_info_11372009 的函數

def call_bus_info(route_id: str):
    """
    呼叫 bus_info_11372009 的 find_bus 函數，並確認執行。
    """
    try:
        print(f"正在查詢公車路線：{route_id}")
        asyncio.run(find_bus(route_id))  # 使用 asyncio 執行異步函數
        print("查詢完成！")
    except Exception as e:
        print(f"執行時發生錯誤：{e}")

# 測試函數
if __name__ == "__main__":
    route_id = input("請輸入公車代碼：").strip()
    call_bus_info(route_id)