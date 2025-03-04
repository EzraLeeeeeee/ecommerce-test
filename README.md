## 預備環境
1. 打開 Anaconda Prompt
2. cd C:\Ezra\專題製作\Project_1\ecommerce-test
3. venv\Scripts\activate

## 執行test_checkout_slow.py   可顯示較慢，使用python方式
1. python tests/test_checkout_slow.py

## 執行自訂登入，加入購物車及填寫收件人資訊完成下單
1. pytest tests/test_checkout.py -v

## 產生測試報告
1. pytest tests/test_checkout.py --browser=chrome --html=reports/report.html --self-contained-html

## CI/CD自動測試
1. git add .
2. git commit -m " 加入 GitHub Actions 自動測試"
3. git push origin main
4. 記得必須使用 無頭模式 (--headless)
