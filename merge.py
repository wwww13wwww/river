import os
import pandas as pd

# 設定資料夾路徑
folder_path = r"C:\river\2024extract"  # 請替換成你的資料夾路徑
# 篩選的 station_id
station_ids_to_filter = [
    "花蓮縣政府水利科",
    "雲林縣政府水利處",
    "嘉義市政府工務處",
    "屏東縣政府水利處"
]
pq_name_to_filter = "淹水深度"  # 篩選條件 PQ_name
# 取得所有以 wra 開頭的檔案
files = [f for f in os.listdir(folder_path) if f.startswith("wra_iow_水利署（與縣市政府合建）_淹水感測器_2024") and f.endswith(".csv")]

# 建立一個空的 DataFrame 用來存儲篩選後的資料
filtered_df = pd.DataFrame()

# 遍歷檔案並篩選資料
for file in files:
    file_path = os.path.join(folder_path, file)
    try:
        # 讀取每個 CSV 檔案
        df = pd.read_csv(file_path)
        
        # 篩選出 Organize_Name 在指定範圍內的資料
        df_filtered = df[(df['Organize_Name'].isin(station_ids_to_filter)) & (df['PQ_name'] == pq_name_to_filter)]
        
        # 按 station_id 分組，計算 value 平均值，並保留其他欄位
        grouped = df_filtered.groupby('station_id', as_index=False).agg({
            'value': 'max',  # 計算 value 平均值
            'Organize_Name': 'first',  # 保留 Organize_Name 的第一筆
            'PQ_name': 'first',  # 保留 PQ_name 的第一筆
            'PQ_fullname': 'first',  # 保留 PQ_fullname 的第一筆
            'Longitude': 'first',  # 保留 Longitude 的第一筆
            'Latitude': 'first',  # 保留 Latitude 的第一筆
            'timestamp': 'first',  # 保留 timestamp 的第一筆
            # 其他需要保留的欄位可以添加在這裡
        })
        
       
        
        # 合併篩選後的資料
        filtered_df = pd.concat([filtered_df, grouped], ignore_index=True)
        print(f"已成功讀取並篩選檔案: {file}")
    except Exception as e:
        print(f"讀取檔案 {file} 時發生錯誤: {e}")

# 儲存篩選後的資料到新的 Excel 檔案
output_file = os.path.join(folder_path, "2024_values_with_columns.xlsx")
try:
    filtered_df.to_excel(output_file, index=False)
    print(f"所有篩選後的檔案已成功合併並儲存至: {output_file}")
except Exception as e:
    print(f"儲存檔案時發生錯誤: {e}")
