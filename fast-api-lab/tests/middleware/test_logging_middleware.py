from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_correlation_id_generated_automatically():
    # 測試 A：客戶端沒傳 Header，服務器自動生成 UUID 並回傳
    response = client.get("/items")
    assert response.status_code == 200
    assert "X-Correlation-ID" in response.headers
    assert "X-Process-Time" in response.headers


def test_correlation_id_passed_by_client():
    # 測試 B：客戶端自己傳入了 Trace ID，服務器繼承該 ID 並原樣帶回
    custom_id = "my-custom-trace-id-12345"
    response = client.get("/items", headers={"X-Correlation-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Correlation-ID"] == custom_id
