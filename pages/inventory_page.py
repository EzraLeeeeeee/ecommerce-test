from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")
        self.add_to_cart_button = (By.XPATH, "//button[text()='Add to cart']")
        self.cart_icon = (By.CLASS_NAME, "shopping_cart_link")

    def sort_items(self, sort_option):
        """ 選擇商品排序方式 """
        dropdown = self.driver.find_element(*self.sort_dropdown)
        dropdown.send_keys(sort_option)

    def add_item_to_cart(self, index=0):
        """加入指定索引的商品到購物車"""
        add_buttons = self.driver.find_elements(By.CLASS_NAME, "btn_inventory")
        if index < len(add_buttons):
            add_buttons[index].click()
        else:
            print(f"❌ 商品索引 {index} 超出範圍")

    def go_to_cart(self):
        """ 點擊購物車按鈕 """
        try:
            # 嘗試使用顯式等待和常規點擊
            WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.cart_icon)
            ).click()
        except ElementClickInterceptedException:
            # 如果常規點擊失敗，使用 JavaScript 點擊
            cart_element = self.driver.find_element(*self.cart_icon)
            self.driver.execute_script("arguments[0].click();", cart_element)

    def add_multiple_items_to_cart(self, item_names):
        """
        加入多個指定的商品到購物車
        :param item_names: 商品名稱的列表，例如 ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        """
        for item_name in item_names:
            item_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            add_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, item_xpath)))
            add_button.click()

    def add_all_items_to_cart(self):
        """
        加入所有商品到購物車
        """
        add_buttons = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(text(), 'Add to cart')]"))
        )

        for button in add_buttons:
            button.click()
        print(f"✅ 成功將 {len(add_buttons)} 件商品加入購物車！")