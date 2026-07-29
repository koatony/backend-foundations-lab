from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_create_item_success():
    payload = {
        "title":"滑鼠",
        "description":"RGB電競滑鼠",
        "price":599.0
    }
    resp = client.post("items", json=payload)
    assert resp.status_code == 201
    data = resp.json()   
    assert data["title"] == "滑鼠"
    assert "id" in data
    assert "created_at" in data   
    