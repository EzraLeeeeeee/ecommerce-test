from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import sys
import os
# 添加當前目錄的上級目錄到 Python 模組搜索路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
import time

def test_add_to_cart():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")

    # 1. 登入
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    time.sleep(2)  # 等待頁面加載

    # 2. 加入商品到購物車
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()

    time.sleep(2)

    assert "cart.html" in driver.current_url, "未成功進入購物車！"
    print("✅ 測試通過，成功加入購物車")
    driver.quit()

if __name__ == "__main__":
    test_add_to_cart()
