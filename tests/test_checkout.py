from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import sys
import os
# 添加當前目錄的上級目錄到 Python 模組搜索路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from selenium.webdriver.common.by import By
import time

def test_complete_checkout():
    # 初始化 Chrome 選項和服務
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    
    # 正確初始化 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")

    try:
        # 1️⃣ 登入
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        time.sleep(2)

        # 2️⃣ 瀏覽商品 & 排序
        inventory_page = InventoryPage(driver)
        inventory_page.sort_items("Price (low to high)")
        time.sleep(2)

        # 3️⃣ 加入商品到購物車並進入購物車頁面
        inventory_page.add_item_to_cart()
        inventory_page.go_to_cart()
        time.sleep(2)

        # 4️⃣ 進入結帳頁面
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # 5️⃣ 填寫結帳資訊
        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_info("Ezra", "Test", "12345")
        time.sleep(2)

        # 6️⃣ 完成下單
        checkout_page.finish_checkout()
        time.sleep(2)

        assert "checkout-complete.html" in driver.current_url, "結帳流程測試失敗"
        print("✅ 測試通過，成功完成結帳！")

    finally:
        driver.quit()



def test_missing_info():
     # 初始化 Chrome 選項和服務
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    
    # 正確初始化 WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")

    # 1️⃣ 登入
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")
    time.sleep(2)

    # 2️⃣ 進入購物車
    inventory_page = InventoryPage(driver)
    inventory_page.add_item_to_cart()
    inventory_page.go_to_cart()
    time.sleep(2)

    # 3️⃣ 進入結帳
    cart_page = CartPage(driver)
    cart_page.proceed_to_checkout()
    time.sleep(2)

    # 4️⃣ 缺少必填資訊
    checkout_page = CheckoutPage(driver)
    checkout_page.enter_checkout_info("", "", "")
    time.sleep(2)

    # 5️⃣ 確認錯誤訊息
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
    assert "Error" in error_message, "錯誤處理測試失敗"
    print("✅ 測試通過，缺少資訊時無法結帳")

    driver.quit()



if __name__ == "__main__":
    test_complete_checkout()
    test_missing_info()