import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 設定 Edge options
options = Options()
options.add_argument("--start-maximized")

# 指定 EdgeDriver 路徑
service = Service(r'C:\Users\User\Downloads\edgedriver_win64\msedgedriver.exe')
driver = webdriver.Edge(service=service, options=options)
url = "https://history.colife.org.tw/#/?cd=%2F%E6%B0%B4%E8%B3%87%E6%BA%90%2F%E6%B0%B4%E5%88%A9%E7%BD%B2_%E6%B7%B9%E6%B0%B4%E6%84%9F%E6%B8%AC%E5%99%A8%2F202306"
driver.get(url)
time.sleep(5)  # 等待網頁完全載入

# 提取下載連結
links = driver.find_elements(By.XPATH, '//a[@href]')
download_links = []
for link in links:
    href = link.get_attribute('href')
    if "/download&path=" in href:
        download_links.append(href)

driver.quit()  # 關閉瀏覽器

# 移除重複連結（如有）
download_links = list(set(download_links))
print(f"找到 {len(download_links)} 筆下載連結")

download_folder = "C:\\Users\\User\\Downloads\\"

# 自動下載檔案
for url in download_links:
    # 解碼並清理檔案名稱
    file_name = url.split("path=")[-1]
    file_name = requests.utils.unquote(file_name)
    
    # 檢查檔案名稱是否符合以 wra_iow_水利署_淹水感測器_202306 開頭
    if file_name.startswith("wra_iow_水利署_淹水感測器_202307"):
        file_name = re.sub(r'[\/:*?"<>|]', '_', file_name)  # 替換非法字元
        file_path = os.path.join(download_folder, file_name)

        print(f"下載中: {url}")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"已下載: {file_name}")
            else:
                print(f"下載失敗: {url}，HTTP 狀態碼: {response.status_code}")
        except Exception as e:
            print(f"下載失敗: {url}，錯誤訊息: {e}")
    else:
        print(f"跳過不符合名稱模式的檔案: {file_name}")

print("所有檔案已下載完成！")
