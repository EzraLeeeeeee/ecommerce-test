import pytest
import os
from datetime import datetime
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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """ 測試失敗時截圖 """
    outcome = yield
    report = outcome.get_result()

    if report.failed:
        # 取得 driver
        driver = item.funcargs.get("driver")
        if driver:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshot_dir = "screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{timestamp}.png")

            driver.save_screenshot(screenshot_path)
            print(f"❌ 測試失敗，已截圖：{screenshot_path}")

def pytest_addoption(parser):
    """ 新增 pytest 命令行參數 """
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: chrome, firefox, or edge")

@pytest.fixture
def driver(request):
    """ 根據參數選擇瀏覽器 """
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = ChromeOptions()
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        options.add_argument("--user-data-dir=/tmp/chrome_test_profile") #确保每次执行时都使用不同的目录路径。

    elif browser == "firefox":
        options = FirefoxOptions()
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        options = EdgeOptions()
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    else:
        raise ValueError("❌ Unsupported browser: Use 'chrome', 'firefox', or 'edge'")

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    yield driver
    driver.quit()