#連結GitHub Actions

import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

@pytest.fixture
def driver(request):
    """ 根據參數選擇瀏覽器 """
    browser = request.config.getoption("--browser", default="chrome")

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")  # 无界面模式
        options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
        options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")  # 无界面模式
        options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
        options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")  # 无界面模式
        options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
        options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    else:
        raise ValueError("❌ Unsupported browser: Use 'chrome', 'firefox', or 'edge'")

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()

class TestCheckout:
    """ 電商網站的結帳測試 """

    def test_complete_checkout(self, driver):
        """ 測試完整結帳流程 """
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        inventory_page = InventoryPage(driver)
        inventory_page.sort_items("Price (low to high)")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        inventory_page.add_item_to_cart()
        inventory_page.go_to_cart()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))

        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_info("Ezra", "Lee", "12345")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_summary_container")))

        checkout_page.finish_checkout()
        WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete.html"))

        assert "checkout-complete.html" in driver.current_url, "❌ 結帳流程測試失敗"
        print("✅ 測試通過，成功完成結帳！")

    def test_missing_info(self, driver):
        """ 測試錯誤處理（缺少必填資訊） """
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

        inventory_page = InventoryPage(driver)
        inventory_page.add_item_to_cart()
        inventory_page.go_to_cart()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))

        checkout_page = CheckoutPage(driver)
        checkout_page.enter_checkout_info("", "", "")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "error-message-container")))

        error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "Error" in error_message, "❌ 錯誤處理測試失敗"
        print("✅ 測試通過，缺少資訊時無法結帳")

















# 沒有無頭模式，可以開啟瀏覽器視窗

# import pytest
# import sys
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from pages.login_page import LoginPage
# from pages.inventory_page import InventoryPage
# from pages.cart_page import CartPage
# from pages.checkout_page import CheckoutPage

# @pytest.fixture
# def driver(request):
#     """ 根據參數選擇瀏覽器 """
#     browser = request.config.getoption("--browser", default="chrome")

#     if browser == "chrome":
#         options = ChromeOptions()
#         # 移除 --headless 參數
#         options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
#         options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
#         service = ChromeService(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)

#     elif browser == "firefox":
#         options = FirefoxOptions()
#         # 移除 --headless 參數
#         options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
#         options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
#         service = FirefoxService(GeckoDriverManager().install())
#         driver = webdriver.Firefox(service=service, options=options)

#     elif browser == "edge":
#         options = EdgeOptions()
#         # 移除 --headless 參數
#         options.add_argument("--no-sandbox")  # 适用于无 root 权限环境
#         options.add_argument("--disable-dev-shm-usage")  # 解决共享内存问题
#         service = EdgeService(EdgeChromiumDriverManager().install())
#         driver = webdriver.Edge(service=service, options=options)

#     else:
#         raise ValueError("❌ Unsupported browser: Use 'chrome', 'firefox', or 'edge'")

#     driver.get("https://www.saucedemo.com/")
#     driver.maximize_window()
#     yield driver
#     driver.quit()

# class TestCheckout:
#     """ 電商網站的結帳測試 """

#     def test_complete_checkout(self, driver):
#         """ 測試完整結帳流程 """
#         login_page = LoginPage(driver)
#         login_page.login("standard_user", "secret_sauce")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

#         inventory_page = InventoryPage(driver)
#         inventory_page.sort_items("Price (low to high)")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

#         inventory_page.add_item_to_cart()
#         inventory_page.go_to_cart()
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

#         cart_page = CartPage(driver)
#         cart_page.proceed_to_checkout()
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))

#         checkout_page = CheckoutPage(driver)
#         checkout_page.enter_checkout_info("Ezra", "Test", "12345")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_summary_container")))

#         checkout_page.finish_checkout()
#         WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete.html"))

#         assert "checkout-complete.html" in driver.current_url, "❌ 結帳流程測試失敗"
#         print("✅ 測試通過，成功完成結帳！")

#     def test_missing_info(self, driver):
#         """ 測試錯誤處理（缺少必填資訊） """
#         login_page = LoginPage(driver)
#         login_page.login("standard_user", "secret_sauce")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

#         inventory_page = InventoryPage(driver)
#         inventory_page.add_item_to_cart()
#         inventory_page.go_to_cart()
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))

#         cart_page = CartPage(driver)
#         cart_page.proceed_to_checkout()
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))

#         checkout_page = CheckoutPage(driver)
#         checkout_page.enter_checkout_info("", "", "")
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "error-message-container")))

#         error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
#         assert "Error" in error_message, "❌ 錯誤處理測試失敗"
#         print("✅ 測試通過，缺少資訊時無法結帳")















# import pytest
# import sys
# import os
# import allure
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from pages.login_page import LoginPage
# from pages.inventory_page import InventoryPage
# from pages.cart_page import CartPage
# from pages.checkout_page import CheckoutPage


# @pytest.fixture
# def driver(request):
#     """ 根據參數選擇瀏覽器 """
#     browser = request.config.getoption("--browser", default="chrome")

#     if browser == "chrome":
#         options = ChromeOptions()
#         options.add_argument("--no-sandbox")  
#         options.add_argument("--disable-dev-shm-usage")
#         service = ChromeService(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)

#     elif browser == "firefox":
#         options = FirefoxOptions()
#         options.add_argument("--no-sandbox")  
#         options.add_argument("--disable-dev-shm-usage")
#         service = FirefoxService(GeckoDriverManager().install())
#         driver = webdriver.Firefox(service=service, options=options)

#     elif browser == "edge":
#         options = EdgeOptions()
#         options.add_argument("--no-sandbox")  
#         options.add_argument("--disable-dev-shm-usage")
#         service = EdgeService(EdgeChromiumDriverManager().install())
#         driver = webdriver.Edge(service=service, options=options)

#     else:
#         raise ValueError("❌ Unsupported browser: Use 'chrome', 'firefox', or 'edge'")

#     driver.get("https://www.saucedemo.com/")
#     driver.maximize_window()
#     yield driver
#     driver.quit()


# @allure.feature("結帳流程")  # Allure 功能標籤
# class TestCheckout:
#     """ 電商網站的結帳測試 """

#     @allure.story("成功結帳")  # Allure 故事標籤
#     @allure.description("測試使用者可以成功完成購物並結帳")  # 描述
#     @allure.severity(allure.severity_level.CRITICAL)  # 設定測試嚴重性
#     def test_complete_checkout(self, driver):
#         """ 測試完整結帳流程 """
#         with allure.step("登入帳號"):
#             login_page = LoginPage(driver)
#             login_page.login("standard_user", "secret_sauce")
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

#         with allure.step("選擇商品並加入購物車"):
#             inventory_page = InventoryPage(driver)
#             inventory_page.sort_items("Price (low to high)")
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
#             inventory_page.add_item_to_cart()
#             inventory_page.go_to_cart()

#         with allure.step("進入購物車並前往結帳"):
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))
#             cart_page = CartPage(driver)
#             cart_page.proceed_to_checkout()

#         with allure.step("輸入結帳資訊並完成結帳"):
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))
#             checkout_page = CheckoutPage(driver)
#             checkout_page.enter_checkout_info("Ezra", "Test", "12345")
#             checkout_page.finish_checkout()

#         with allure.step("驗證是否成功結帳"):
#             WebDriverWait(driver, 10).until(EC.url_contains("checkout-complete.html"))
#             assert "checkout-complete.html" in driver.current_url, "❌ 結帳流程測試失敗"

#         allure.attach(driver.get_screenshot_as_png(), name="checkout_success", attachment_type=allure.attachment_type.PNG)
#         print("✅ 測試通過，成功完成結帳！")

#     @allure.story("缺少結帳資訊")  
#     @allure.description("測試缺少結帳資訊時應顯示錯誤訊息")  
#     @allure.severity(allure.severity_level.NORMAL)
#     def test_missing_info(self, driver):
#         """ 測試錯誤處理（缺少必填資訊） """
#         with allure.step("登入帳號"):
#             login_page = LoginPage(driver)
#             login_page.login("standard_user", "secret_sauce")
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))

#         with allure.step("選擇商品並加入購物車"):
#             inventory_page = InventoryPage(driver)
#             inventory_page.add_item_to_cart()
#             inventory_page.go_to_cart()

#         with allure.step("進入購物車並前往結帳"):
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))
#             cart_page = CartPage(driver)
#             cart_page.proceed_to_checkout()

#         with allure.step("輸入空白結帳資訊"):
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "checkout_info")))
#             checkout_page = CheckoutPage(driver)
#             checkout_page.enter_checkout_info("", "", "")

#         with allure.step("驗證錯誤訊息是否顯示"):
#             WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "error-message-container")))
#             error_message = driver.find_element(By.CLASS_NAME, "error-message-container").text
#             assert "Error" in error_message, "❌ 錯誤處理測試失敗"

#         allure.attach(driver.get_screenshot_as_png(), name="missing_info_error", attachment_type=allure.attachment_type.PNG)
#         print("✅ 測試通過，缺少資訊時無法結帳")
