from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import sys
import os
import time

# 添加目錄到 Python 路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def setup_driver():
    """設置並返回 WebDriver"""
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    return driver

def test_complete_checkout():
    """測試完整結帳流程"""
    try:
        driver = setup_driver()
        
        # 1️⃣ 登入
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        time.sleep(2)

        # 2️⃣ 瀏覽商品 & 排序
        inventory_page = InventoryPage(driver)
        inventory_page.sort_items("Price (low to high)")
        time.sleep(2)

        # 3️⃣ 加入商品到購物車並進入購物車頁面
        # inventory_page.add_item_to_cart(index=0)  # 加入第一個商品
        # inventory_page.add_item_to_cart(index=1)  # 加入第二個商品
        # inventory_page.add_item_to_cart(index=2)  # 加入第三個商品

        # 3️⃣ 加入所有商品到購物車
        for i in range(6):  # SauceDemo 有 6 個商品
            inventory_page.add_item_to_cart(index=i)

        inventory_page.go_to_cart()
        time.sleep(2)

        # 4️⃣ 進入結帳頁面
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # 5️⃣ 填寫結帳資訊
        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_info("Ezra", "Lee", "12345")
        time.sleep(2)

        # 6️⃣ 完成下單
        checkout_page.finish_checkout()
        time.sleep(2)

        # 驗證結果
        assert "checkout-complete.html" in driver.current_url, "❌ 結帳流程測試失敗"
        print("✅ 測試通過，成功完成結帳！")

    except Exception as e:
        print(f"❌ 測試失敗：{str(e)}")
        # 保存錯誤截圖
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        driver.save_screenshot(f"error_screenshot_{timestamp}.png")
        raise
    
    finally:
        driver.quit()

def test_missing_info():
    """測試錯誤處理（缺少必填資訊）"""
    try:
        driver = setup_driver()

        # 1️⃣ 登入
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        time.sleep(2)

        # 2️⃣ 加入商品到購物車
        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart()
        inventory_page.go_to_cart()
        time.sleep(2)

        # 3️⃣ 進入結帳頁面
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        time.sleep(2)

        # 4️⃣ 測試空白資訊
        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_info("", "", "")
        time.sleep(2)

        # 驗證錯誤訊息
        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "Error" in error_message, "❌ 錯誤處理測試失敗"
        print("✅ 測試通過，缺少資訊時無法結帳")

    except Exception as e:
        print(f"❌ 測試失敗：{str(e)}")
        # 保存錯誤截圖
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        driver.save_screenshot(f"error_screenshot_{timestamp}.png")
        raise
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("開始執行完整結帳流程測試...")
    test_complete_checkout()
    print("\n開始執行缺少資訊測試...")
    test_missing_info()