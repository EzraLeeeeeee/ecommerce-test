import requests
import pytest
import allure

BASE_URL = "https://fakestoreapi.com"

@allure.feature("登入 API")
def test_login():
    """測試登入 API 並獲取 Token"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "johnd",
        "password": "m38rmF$"
    }
    response = requests.post(url, json=payload)
    
    assert response.status_code == 200, f"登入失敗，狀態碼: {response.status_code}"
    json_data = response.json()
    
    assert "token" in json_data, "回應中沒有 Token"
    
    # 將 token 存入 pytest 變數
    pytest.auth_token = json_data["token"]
    print("✅ 登入成功，Token:", pytest.auth_token)

@allure.feature("獲取產品列表 API")
def test_get_products():
    """測試獲取產品列表 API"""
    url = f"{BASE_URL}/products"
    headers = {"Authorization": f"Bearer {pytest.auth_token}"}
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, f"獲取產品列表失敗，狀態碼: {response.status_code}"
    json_data = response.json()
    
    assert isinstance(json_data, list), "產品列表應該是 JSON 陣列"
    assert len(json_data) > 0, "產品列表不應該是空的"
    print("✅ 產品列表獲取成功，產品數量:", len(json_data))

@allure.feature("下單 API")
def test_create_order():
    """測試下單 API"""
    url = f"{BASE_URL}/carts"
    headers = {"Authorization": f"Bearer {pytest.auth_token}"}
    payload = {
        "userId": 1,
        "date": "2024-02-21",
        "products": [
            {"productId": 1, "quantity": 2},
            {"productId": 3, "quantity": 1}
        ]
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    assert response.status_code == 200, f"下單失敗，狀態碼: {response.status_code}"
    json_data = response.json()
    
    assert "id" in json_data, "回應中沒有訂單 ID"
    print("✅ 下單成功，訂單 ID:", json_data["id"])
