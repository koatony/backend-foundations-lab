# tests/repositories/test_task_repository_db.py

import pytest
from datetime import datetime, timezone
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# 1. 引入真實的 Base、TaskModel 與相關結構
from app.database import Base
from app.models.task import TaskModel
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate


from app.exceptions.exceptions import TaskNotFoundError

# === 1. 建立記憶體資料庫 (In-memory Database) ===
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    每個測試使用一個乾淨的記憶體 SQLite 資料庫。
    """
    # 建立記憶體引擎
    engine = create_engine("sqlite:///:memory:")
    
    # 建立所有測試用的 Model (透過 app.database 匯入的 Base，會自動抓到已註冊的 TaskModel)
    Base.metadata.create_all(engine)
    
    # 建立 Session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()

# === 2. 定義 TaskRepository 注入器 ===
@pytest.fixture(scope="function")
def task_repo(db_session: Session) -> TaskRepository:
    return TaskRepository(db=db_session)

# === 3. 測試實作 ===

def test_create_task(task_repo: TaskRepository, db_session: Session):
    # 準備建立資料 (priority 須為大寫)
    task_create = TaskCreate(
        title="Buy Groceries",
        description="Milk, Eggs, Bread",
        priority="HIGH"
    )
    
    # 執行建立
    created_task = task_repo.create(task_create)
    
    # 【鐵證驗證】直接向 db_session 查詢，確認資料真的寫入資料庫！
    db_task = db_session.query(TaskModel).filter(TaskModel.id == created_task.id).first()
    
    assert db_task is not None
    assert db_task.title == "Buy Groceries"
    assert db_task.description == "Milk, Eggs, Bread"
    assert db_task.priority == "HIGH"
    assert db_task.status == "TODO"  # 預設狀態應為 TODO
    assert db_task.created_at is not None
    assert db_task.updated_at is None
    

def test_get_by_id(task_repo: TaskRepository, db_session: Session):
    # 1. 直接向 db_session 寫入一筆測試資料
    db_task = TaskModel(
        id="test-id-123",
        title="Database Task",
        description="Write directly to DB",
        priority="LOW",
        status="TODO"
    )
    db_session.add(db_task)
    db_session.commit()
    
    # 2. 嘗試用 Repository 查詢
    found = task_repo.get_by_id("test-id-123")
    
    # 3. 驗證撈出來的資料是否正確
    assert found is not None
    assert found.id == "test-id-123"
    assert found.title == "Database Task"

def test_get_by_id_not_found(task_repo: TaskRepository):
    result = task_repo.get_by_id("non-existent-id")
    assert result is None

def test_list_all(task_repo: TaskRepository, db_session: Session):
    # 1. 直接向 db_session 寫入兩筆資料
    db_session.add(TaskModel(id="T1", title="Task 1", priority="HIGH", status="TODO"))
    db_session.add(TaskModel(id="T2", title="Task 2", priority="MEDIUM", status="TODO"))
    db_session.commit()
    
    # 2. 用 Repository 查詢列表
    tasks = task_repo.list_all()
    
    # 3. 驗證
    assert len(tasks) == 2
    titles = [t.title for t in tasks]
    assert "Task 1" in titles
    assert "Task 2" in titles

def test_update_task(task_repo: TaskRepository, db_session: Session):
    # 1. 寫入原始資料
    db_task = TaskModel(id="T-Update", title="Original", description="Desc", priority="LOW", status="TODO")
    db_session.add(db_task)
    db_session.commit()
    
    # 2. 準備更新資料
    task_update = TaskUpdate(
        title="Updated",
        priority="HIGH",
        description=None  # 保持 description 不變
    )
    
    # 執行更新
    task_repo.update("T-Update", task_update)
    
    # 【鐵證驗證】直接向 db_session 重新查詢，確認資料庫內的值被改寫了
    db_refetched = db_session.query(TaskModel).filter(TaskModel.id == "T-Update").first()
    assert db_refetched.title == "Updated"  # 已更新
    assert db_refetched.priority == "HIGH"   # 已更新
    assert db_refetched.description == "Desc" # 保持原樣

def test_update_task_not_found(task_repo: TaskRepository):
    task_update = TaskUpdate(title="Not Found", priority="HIGH")
    
    result = task_repo.update("non-existent-id", task_update)
    assert result is None
    

    

def test_delete_task(task_repo: TaskRepository, db_session: Session):
    # 1. 寫入待刪資料
    db_task = TaskModel(id="T-Delete", title="To Delete", priority="LOW", status="TODO")
    db_session.add(db_task)
    db_session.commit()
    
    # 2. 執行刪除
    deleted = task_repo.delete("T-Delete")
    assert deleted is True
    
    # 【鐵證驗證】直接用 db_session 查詢，確認資料庫已經完全沒有這筆資料
    db_refetched = db_session.query(TaskModel).filter(TaskModel.id == "T-Delete").first()
    assert db_refetched is None

def test_delete_task_not_found(task_repo: TaskRepository):
    deleted = task_repo.delete("non-existent-id")
    assert deleted is False




# 測試Rollback
def test_transaction_rollback_on_error(task_repo:TaskRepository, db_session:Session):
    

    task1 = TaskModel(title="Task1", priority="HIGH", status="TODO")
    
    try:
        db_session.add(task1)
        db_session.flush()

        raise RuntimeError("模擬系統崩潰")

        db_session.commit()

    except Exception as e:
        print(str(e))
        db_session.rollback()



    saved_tasks = task_repo.list_all()    
    assert len(saved_tasks) == 0
    