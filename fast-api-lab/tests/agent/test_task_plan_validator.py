import pytest
from app.schemas.task_plan import TaskPlan, TaskItem, DependencyValidationResult
from app.utils.task_validator import validate_task_dependencies

@pytest.fixture
def mock_data_no_dep() -> TaskPlan:
    task_item1 = TaskItem(
        task_id="T1",
        title="任務1",
        description="任務1的描述",
        priority="High",
        estimated_hours=1.0,
        dependencies=[],
        acceptance_criteria=[]
    )
    task_item2 = TaskItem(
        task_id="T2",
        title="任務2",
        description="任務2的描述",
        priority="Medium",
        estimated_hours=2.0,
        dependencies=["T1"],
        acceptance_criteria=[]
    )
    task_item3 = TaskItem(
        task_id="T3",
        title="任務3",
        description="任務3的描述",
        priority="Low",
        estimated_hours=3.0,
        dependencies=["T1", "T2"],
        acceptance_criteria=[]
    )
    task_plan = TaskPlan(
        project_name="測試專案",
        summary="這是測試專案的摘要",
        tasks=[task_item1, task_item2, task_item3]
    )
    return task_plan

@pytest.fixture
def mock_data_with_dep() -> TaskPlan:
    task_item1 = TaskItem(
        task_id="T1",
        title="任務1",
        description="任務1的描述",
        priority="High",
        estimated_hours=1.0,
        dependencies=["T2"],
        acceptance_criteria=[]
    )
    task_item2 = TaskItem(
        task_id="T2",
        title="任務2",
        description="任務2的描述",
        priority="Medium",
        estimated_hours=2.0,
        dependencies=["T1"],
        acceptance_criteria=[]
    )
    task_item3 = TaskItem(
        task_id="T3",
        title="任務3",
        description="任務3的描述",
        priority="Low",
        estimated_hours=3.0,
        dependencies=["T1", "T2"],
        acceptance_criteria=[]
    )
    task_plan = TaskPlan(
        project_name="測試專案",
        summary="這是測試專案的摘要",
        tasks=[task_item1, task_item2, task_item3]
    )
    return task_plan

@pytest.fixture
def anticipated_result_no_dep():
    return DependencyValidationResult(
        is_valid=True,
        missing_dependencies=[],
        has_cycle=False,
        cycle_path=[],
        error_messages=[]
    )

def test_validate_task_dependencies_success(mock_data_no_dep, anticipated_result_no_dep):
    result = validate_task_dependencies(mock_data_no_dep)
    assert result == anticipated_result_no_dep

def test_validate_task_dependencies_with_cycle(mock_data_with_dep):
    result = validate_task_dependencies(mock_data_with_dep)
    assert result.is_valid is False
    assert result.has_cycle is True
    assert result.cycle_path == ["T1", "T2", "T1"]
    assert result.missing_dependencies == []
    assert result.error_messages == ["任務之間存在循環依賴: T1 -> T2 -> T1"]

# 1. 檢查Task ID 重複
def test_validate_task_dependencies_duplicate_id():
    task_item1 = TaskItem(
        task_id="T1",
        title="任務1",
        description="描述",
        priority="High",
        estimated_hours=1.0,
        dependencies=[],
        acceptance_criteria=[]
    )
    task_item2 = TaskItem(
        task_id="T1",  # 重複 ID
        title="重複的任務1",
        description="描述",
        priority="Medium",
        estimated_hours=2.0,
        dependencies=[],
        acceptance_criteria=[]
    )
    plan = TaskPlan(
        project_name="重複ID測試",
        summary="摘要",
        tasks=[task_item1, task_item2]
    )
    result = validate_task_dependencies(plan)
    assert result.is_valid is False
    assert "重複" in result.error_messages[0]
    assert result.has_cycle is False

# 2. 檢查依賴的 Task ID 是否存在
def test_validate_task_dependencies_missing_dep():
    task_item1 = TaskItem(
        task_id="T1",
        title="任務1",
        description="描述",
        priority="High",
        estimated_hours=1.0,
        dependencies=["T99"],  # 依賴不存在的任務
        acceptance_criteria=[]
    )
    plan = TaskPlan(
        project_name="缺失依賴測試",
        summary="摘要",
        tasks=[task_item1]
    )
    result = validate_task_dependencies(plan)
    assert result.is_valid is False
    assert "T99" in result.missing_dependencies
    assert "不存在" in result.error_messages[0]
    assert result.has_cycle is False