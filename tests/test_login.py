from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sys
import os
# 添加當前目錄的上級目錄到 Python 模組搜索路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage
import time

def test_login():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")
    
    login_page = LoginPage(driver)
    login_page.login("standard_user", "secret_sauce")

    time.sleep(2)  # 等待頁面加載
    assert "inventory.html" in driver.current_url, "登入失敗！"

    print("✅ 測試通過，成功登入 SauceDemo")
    driver.quit()


def test_invalid_login():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.saucedemo.com/")

    login_page = LoginPage(driver)
    login_page.login("standard_user", "wrong_password")

    time.sleep(2)
    error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text

    assert "Epic sadface" in error_message, "錯誤密碼測試失敗"
    print("✅ 測試通過，錯誤密碼登入失敗")
    driver.quit()



if __name__ == "__main__":
    test_login()
    test_invalid_login()
