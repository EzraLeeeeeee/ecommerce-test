## 預備環境
1. 打開 Anaconda Prompt
2. cd C:\Ezra\專題製作\Project_1\ecommerce-test
3. venv\Scripts\activate

## 執行自動登入程序
1. python tests/test_login.py
or
1. pytest tests/test_login.py -v

## 執行自動登入及加入購物車程序
1. python tests/test_add_to_cart.py
or
2. pytest tests/test_add_to_cart.py -v

## 執行自訂登入，加入購物車及填寫收件人資訊完成下單
1. python tests/test_checkout.py
or
2. pytest tests/test_checkout.py -v