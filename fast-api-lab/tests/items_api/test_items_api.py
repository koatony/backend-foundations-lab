import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import _repo


@pytest.fixture(autouse=True)
def clear_repo():
    """每個測試案例執行前自動清空 repository 記憶體」"""
    _repo._storage.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_create_item_api_success(client):
    payload = {
        "title": "聯想筆電",
        "description": "高效能工作站",
        "price": 35000.0
    }
    resp = client.post("/items", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "聯想筆電"
    assert "id" in data


def test_create_item_api_duplicate_conflict(client):
    payload = {
        "title": "獨立耳機",
        "price": 1200.0
    }
    client.post("/items", json=payload)

    # 再次發送相同的 title 應該被捕捉為 DuplicateItemError 並返回 409 Conflict
    resp = client.post("/items", json=payload)
    assert resp.status_code == 409
    data = resp.json()
    assert data["code"] == "DUPLICATE_ITEM"


def test_get_item_api_not_found(client):
    resp = client.get("/items/non-existent-id")
    assert resp.status_code == 404
    data = resp.json()
    assert data["code"] == "NOT_FOUND"


def test_list_items_api(client):
    client.post("/items", json={"title": "鍵盤", "price": 1000.0})
    client.post("/items", json={"title": "螢幕", "price": 5000.0})

    resp = client.get("/items")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


