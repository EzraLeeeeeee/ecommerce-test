from selenium.webdriver.common.by import By

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
        self.driver.find_element(*self.cart_icon).click()

