import os
import zipfile

# 下載的檔案所在的資料夾
download_folder = r'C:\river\2024'

# 壓縮檔案的檔名格式
file_prefix = "wra_iow_水利署（與縣市政府合建）_淹水感測器_202406"
file_extension = ".zip"

# 假設解壓縮範圍是 20240601 到 20240630
for day in range(1, 32):
    # 格式化日期，確保是 8 位數，例如 20240601
    date_str = f"{day:02d}"

    # 完整的壓縮檔案名稱
    file_name = f"{file_prefix}{date_str}{file_extension}"
    file_path = os.path.join(download_folder, file_name)

    # 檢查檔案是否存在
    if os.path.exists(file_path):
        try:
            # 開啟並解壓縮檔案
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # 解壓縮至指定資料夾
                extract_folder = r'C:\river\2024extract'
                os.makedirs(extract_folder, exist_ok=True)
                zip_ref.extractall(extract_folder)
                print(f"已解壓縮: {file_name} 至 {extract_folder}")
        except zipfile.BadZipFile:
            print(f"檔案 {file_name} 不是有效的壓縮檔案，跳過！")
        except Exception as e:
            print(f"解壓縮檔案 {file_name} 時發生錯誤: {e}")
    else:
        print(f"檔案 {file_name} 不存在，跳過！")

print("所有檔案已解壓縮完成！")
