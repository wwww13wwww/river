from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 設定 Edge options
options = Options()
options.add_argument("--start-maximized")

# 指定 EdgeDriver 路徑
service = Service(r'C:\Users\User\Downloads\edgedriver_win64\msedgedriver.exe')
driver = webdriver.Edge(service=service, options=options)

# 測試 Edge 瀏覽器
driver.get("https://www.google.com")
