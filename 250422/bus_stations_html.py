import folium
import json

def leafjet_plot_bus(input_path: str, output_path: str):
    
    # 讀取 GeoJSON 檔案
    with open(input_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # 建立地圖，設定中心點和縮放級別
    m = folium.Map(location=[25.0330, 121.5654], zoom_start=13)  # 台北市中心

    # 將 GeoJSON 資料加入地圖
    folium.GeoJson(geojson_data, name="geojson").add_to(m)

    # 加入圖層控制
    folium.LayerControl().add_to(m)

    # 將地圖儲存為 HTML
    m.save(output_path)
    print(f"地圖已儲存為 {output_path}")

# 測試函數
if __name__ == "__main__":
    input_path = input("請輸入 GeoJSON 檔案路徑：").strip()  # 替換為您的 GeoJSON 檔案名稱
    output_path = input("請輸入檔案儲存路徑：").strip()  # 輸出的 HTML 檔案名稱
    leafjet_plot_bus(input_path, output_path)