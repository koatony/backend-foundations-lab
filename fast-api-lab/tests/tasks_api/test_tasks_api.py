import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_task_service
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService



# 建立初始化資料
@pytest.fixture
def created_task(client):
    payload = {
        "title":"test",
        "description":"test",
        "priority":"HIGH"
    }
    resp = client.post("/tasks",json=payload)
    assert resp.status_code == 201
    return resp.json()

@pytest.fixture
def client():
    """每個測試案例前建立全新的 TaskRepository，並以 dependency_overrides 注入"""
    # TODO: 待重構。因為 TaskRepository 現在需要傳入 db 參數，此處需要改為覆蓋 get_db 以使用記憶體資料庫
    # 現在先暫時註解起來，避免 NameError 與 TypeError 造成專案報錯而無法啟動
    # repo = TaskRepository()
    # task_service = TaskService(repo)
    # app.dependency_overrides[get_task_service] = lambda: task_service

    yield TestClient(app)
    app.dependency_overrides.clear()


# ==============================================================================
# 1. 建立任務 API 測試
# ==============================================================================

def test_create_task_api_success(client):
    """
    [測試情境 1] 正常建立任務 (POST /tasks)
    [預期結果] status_code == 201，且回傳 JSON 包含 id 與 status == "TODO"
    """
    payload ={"title":"test","description":"test","priority":"HIGH"}
    resp = client.post("/tasks",json=payload)
    assert resp.status_code == 201
    assert resp.json()["title"] == "test"
    assert resp.json()["status"] == "TODO"
    assert "id" in resp.json()
    


# ==============================================================================
# 2. 查詢任務 API 測試
# ==============================================================================

def test_get_task_api_success(client,created_task):
    """
    [測試情境 2] 先 POST 建立一筆任務，再透過 GET /tasks/{id} 查詢
    [預期結果] status_code == 200，且能正確查得該任務詳細資訊
    """

    task_id = created_task["id"]
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "test"
    assert resp.json()["status"] == "TODO"
    assert "id" in resp.json()
    
    


def test_get_task_api_not_found(client,created_task):
    """
    [測試情境 3] 查詢不存在的任務 (GET /tasks/non-existent-id)
    [預期結果] status_code == 404，且回傳的錯誤代碼 (code) 為 "NOT_FOUND"
    """
    
    resp = client.get("/tasks/non-existent-id")
    assert resp.status_code == 404
    assert resp.json()["code"] == "NOT_FOUND"
    assert resp.json()["message"] == "任務ID non-existent-id 不存在於資料庫中"
    


# ==============================================================================
# 3. 更新任務 API 測試
# ==============================================================================

def test_update_task_api_success(client,created_task):
    """
    [測試情境 4] 更新任務的標題或狀態 (PUT /tasks/{id})
    [預期結果] status_code == 200，且回傳的任務資訊已被更新
    """
    task_id = created_task["id"]
    resp = client.put(f"/tasks/{task_id}",json={"title":"new","description":"new","priority":"LOW", "status":"DONE"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "new"
    assert resp.json()["description"] == "new"
    assert resp.json()["priority"] == "LOW"
    assert resp.json()["status"] == "DONE"
    assert resp.json()["updated_at"] != resp.json()["created_at"]
    assert "id" in resp.json()
    
    


# ==============================================================================
# 4. 刪除任務 API 測試
# ==============================================================================

def test_delete_task_api_success(client,created_task):
    """
    [測試情境 5] 刪除任務 (DELETE /tasks/{id})
    [預期結果] status_code == 204 (No Content)，且後續查詢該 ID 應回傳 404
    """
    task_id = created_task["id"]
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    resp = client.get(f"/tasks/{task_id}")
    assert resp.status_code == 404
    assert resp.json()["code"] == "NOT_FOUND"
    assert resp.json()["message"] == f"任務ID {task_id} 不存在於資料庫中"
