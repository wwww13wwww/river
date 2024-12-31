import pandas as pd
import os

# 檔案名稱與資料夾
data_file = '2024_values_with_columns.xlsx'
download_folder = r'C:\river'
data_path = os.path.join(download_folder, data_file)

# 讀取 Excel 檔案
try:
    df = pd.read_excel(data_path)
    print("檔案成功讀取！")
except Exception as e:
    print(f"讀取檔案時發生錯誤: {e}")
    exit()

# 清理欄位名稱
df.columns = df.columns.str.strip()

# 列印資料框的欄位名稱
print("原始資料框的欄位名稱：", df.columns.tolist())

# 確保 timestamp 欄位為日期格式
if 'timestamp' in df.columns:
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# 按照 'station_id' 和 'year_month' 分組，找到最大值
if 'station_id' in df.columns and 'year_month' in df.columns and 'value' in df.columns:
    # 找到每組的最大值索引
    idx = df.groupby(['station_id', 'year_month'])['value'].idxmax()
    max_values = df.loc[idx].reset_index(drop=True)  # 保留原資料框中與最大值對應的所有欄位
    print("max_values 資料框生成成功！")
else:
    print("必要的欄位缺失，請檢查資料。")
    exit()

# 檢查結果
print("取最大值後的結果：")
print(max_values.head())

# 保存結果
output_file = 'monthly_station_max_values.xlsx'
try:
    max_values.to_excel(output_file, index=False)
    print(f"結果已保存至 {output_file}")
except Exception as e:
    print(f"保存結果時發生錯誤: {e}")
