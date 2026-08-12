from datetime import datetime, timezone
from unittest.mock import MagicMock
import pytest

from app.exceptions.exceptions import TaskNotFoundError
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService


@pytest.fixture
def mock_repo():
    """建立 Mock 版的 TaskRepository"""
    return MagicMock()


@pytest.fixture
def task_service(mock_repo):
    """注入 Mock Repository 到 TaskService"""
    return TaskService(mock_repo)


# ==============================================================================
# 1. create_task 測試
# ==============================================================================

def test_create_task_success(task_service, mock_repo):
    """
    [測試情境 1] 正常建立任務
    [預期結果] 呼叫 repo.create 並回傳建立好的物件
    """
    test_create_item = TaskCreate(
        title = "test task",
        description = "test desc",
        priority = "HIGH"
    )

    mock_repo.create.return_value = TaskResponse(
        id = "task-1",
        title = "test task",
        description = "test desc",
        priority = "HIGH",
        status = "TODO",
        created_at = datetime.now(timezone.utc),
        updated_at = datetime.now(timezone.utc)
    )
    
    result = task_service.create_task(test_create_item)
    assert result.title == "test task"
    assert result.description == "test desc"
    assert result.priority == "HIGH"
    assert result.status == "TODO"
    assert result.id == "task-1"

    mock_repo.create.assert_called_once_with(test_create_item)


# ==============================================================================
# 2. list_tasks 測試
# ==============================================================================

def test_list_tasks_success(task_service, mock_repo):
    """
    [測試情境 2] 取得任務清單
    [預期結果] 呼叫 repo.list_all 並回傳列表
    """
    task_list = [
        TaskResponse(
            id = "task-1",
            title = "test task",
            description = "test desc",
            priority = "HIGH",
            status = "TODO",
            created_at = datetime.now(timezone.utc),
            updated_at = datetime.now(timezone.utc)
        ),
        TaskResponse(
            id = "task-2",
            title = "test task 2",
            description = "test desc 2",
            priority = "MEDIUM",
            status = "TODO",
            created_at = datetime.now(timezone.utc),
            updated_at = datetime.now(timezone.utc)
        )
    ]

    mock_repo.list_all.return_value = task_list

    result = task_service.list_tasks()

    assert result == task_list
    mock_repo.list_all.assert_called_once()


# ==============================================================================
# 3. get_by_id 測試
# ==============================================================================

def test_get_by_id_success(task_service, mock_repo):
    """
    [測試情境 3] 成功查詢特定 ID
    [預期結果] 回傳對應的 Task 物件
    """
    mock_test = TaskResponse(
        id = "task-1",
        title = "test task",
        description = "test desc",
        priority = "HIGH",
        status = "TODO",
        created_at = datetime.now(timezone.utc),
        updated_at = datetime.now(timezone.utc)
    )
    mock_repo.get_by_id.return_value = mock_test
    
    result = task_service.get_by_id("task-1")
    assert result == mock_test
    mock_repo.get_by_id.assert_called_once_with("task-1")


def test_get_by_id_not_found(task_service, mock_repo):
    """
    [測試情境 4] 查無 ID（異常）
    [預期結果] 拋出 TaskNotFoundError
    """
    mock_repo.get_by_id.return_value = None
    with pytest.raises(TaskNotFoundError):
        task_service.get_by_id("non-existent-id")



# ==============================================================================
# 4. update_task 測試
# ==============================================================================

def test_update_task_success(task_service, mock_repo):
    """
    [測試情境 5] 成功更新任務
    [預期結果] 回傳更新後的 Task 物件
    """
    mock_existing_task = TaskResponse(
        id="task-1",
        title="test task",
        description="test desc",
        priority="HIGH",
        status="TODO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    mock_update_data = TaskUpdate(
        title="test task",
        description="test desc",
        priority="HIGH",
        status="TODO",
    )

    mock_repo.update.return_value = mock_existing_task

    result = task_service.update_task("task-1", mock_update_data)

    assert result == mock_existing_task
    mock_repo.update.assert_called_once_with("task-1", mock_update_data)


def test_update_task_not_found(task_service, mock_repo):
    """
    [測試情境 6] 更新不存在的 ID（異常）
    [預期結果] 拋出 TaskNotFoundError
    """
    mock_repo.update.return_value = None
    

    with pytest.raises(TaskNotFoundError):
        task_service.update_task("non-existent-id", TaskUpdate(
            title="test task",
            description="test desc",
            priority="HIGH",
            status="TODO",
        ))


# ==============================================================================
# 5. delete_task 測試
# ==============================================================================

def test_delete_task_success(task_service, mock_repo):
    """
    [測試情境 7] 成功刪除任務
    [預期結果] 呼叫 repo.delete 並回傳 True
    """
    mock_item = TaskResponse(
        id="task-1",
        title="test task",
        description="test desc",
        priority="HIGH",
        status="TODO",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    mock_repo.get_by_id.return_value = mock_item
    mock_repo.delete.return_value = True

    result = task_service.delete_task("task-1")
    
    assert result is True
    mock_repo.get_by_id.assert_called_once_with("task-1")
    mock_repo.delete.assert_called_once_with("task-1")
    


def test_delete_task_not_found(task_service, mock_repo):
    """
    [測試情境 8] 刪除不存在的 ID（異常）
    [預期結果] 拋出 TaskNotFoundError
    """
    mock_repo.get_by_id.return_value = None
    with pytest.raises(TaskNotFoundError):
        task_service.delete_task("non-existent-id")