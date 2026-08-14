import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_task_service
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from app.database import Base
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dependencies import get_db


from app.models import TaskModel
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


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    每個測試使用一個乾淨的記憶體 SQLite 資料庫。
    """
    # 建立記憶體引擎
    engine = create_engine("sqlite:///:memory:",connect_args={"check_same_thread":False},poolclass=StaticPool)
    
    # 建立所有測試用的 Model (透過 app.database 匯入的 Base，會自動抓到已註冊的 TaskModel)
    Base.metadata.create_all(engine)
    
    # 建立 Session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()





@pytest.fixture
def client(db_session):
    """每個測試案例前建立全新的 TaskRepository，並以 dependency_overrides 注入"""
    # TODO: 待重構。因為 TaskRepository 現在需要傳入 db 參數，此處需要改為覆蓋 get_db 以使用記憶體資料庫
    # 現在先暫時註解起來，避免 NameError 與 TypeError 造成專案報錯而無法啟動
    # repo = TaskRepository()
    # task_service = TaskService(repo)
    # app.dependency_overrides[get_task_service] = lambda: task_service

    app.dependency_overrides[get_db] = lambda: db_session

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


def test_list_tasks_with_pagination(client):
    # 發送 GET /tasks?skip=0&limit=2，斷言回傳陣列長度與 JSON 內容。
    payload1 ={"title":"test1","description":"test","priority":"HIGH"}
    payload2 ={"title":"test2","description":"test","priority":"HIGH"}
    payload3 ={"title":"test3","description":"test","priority":"HIGH"}
    resp1 = client.post("/tasks",json=payload1)
    resp2 = client.post("/tasks",json=payload2)
    resp3 = client.post("/tasks",json=payload3)
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    assert resp3.status_code == 201


    resp = client.get("/tasks", params={"skip": 0, "limit": 2})
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    assert resp.json()[0]["title"] == "test1"
    assert resp.json()[1]["title"] == "test2"
    
    
    
    
    

def test_list_tasks_with_status_filter(client):
    # 發送 GET /tasks?status=TODO，斷言只包含 TODO 狀態的任務。

    payload1 ={"title":"test1","description":"test","priority":"HIGH"}
    payload2 ={"title":"test2","description":"test","priority":"HIGH"}
    payload3 ={"title":"test3","description":"test","priority":"HIGH"}
    resp1 = client.post("/tasks",json=payload1)
    resp2 = client.post("/tasks",json=payload2)
    resp3 = client.post("/tasks",json=payload3)
    assert resp1.status_code == 201
    assert resp2.status_code == 201
    assert resp3.status_code == 201

    resp = client.put(f"/tasks/{resp1.json()["id"]}",json={"status":"DONE"})
    


    resp = client.get("/tasks", params={"status": "TODO"})
    assert resp.status_code == 200
    assert len(resp.json()) == 2
    assert resp.json()[0]["title"] == "test2"
    assert resp.json()[1]["title"] == "test3"
    assert resp.json()[0]["status"] == "TODO"
    assert resp.json()[1]["status"] == "TODO"