import pytest
from app.schemas.task_plan import TaskPlan, TaskItem, validate_task_dependencies


def test_validate_task_dependencies_valid_dag():
    # Arrange: 合法的 DAG 依賴結構 (T1 <- T2 <- T3)
    task_plan = TaskPlan(
        project_name="Valid DAG Project",
        summary="A project without circular dependencies or missing IDs",
        tasks=[
            TaskItem(
                task_id="T1",
                title="Task 1",
                description="Root task",
                priority="High",
                estimated_hours=1.0,
                dependencies=[],
                acceptance_criteria=[]
            ),
            TaskItem(
                task_id="T2",
                title="Task 2",
                description="Depends on T1",
                priority="Medium",
                estimated_hours=2.0,
                dependencies=["T1"],
                acceptance_criteria=[]
            ),
            TaskItem(
                task_id="T3",
                title="Task 3",
                description="Depends on T2",
                priority="Low",
                estimated_hours=3.0,
                dependencies=["T2"],
                acceptance_criteria=[]
            ),
        ]
    )

    # Act
    result = validate_task_dependencies(task_plan)

    # Assert
    assert result.is_valid is True
    assert result.has_cycle is False
    assert result.missing_dependencies == []
    assert result.cycle_path == []
    assert result.error_messages == []


def test_validate_task_dependencies_missing_id():
    # Arrange: T2 依賴了不存在的任務 ID "T99"
    task_plan = TaskPlan(
        project_name="Missing Dependency Project",
        summary="Project with a missing task ID dependency",
        tasks=[
            TaskItem(
                task_id="T1",
                title="Task 1",
                description="Root task",
                priority="High",
                estimated_hours=1.0,
                dependencies=[],
                acceptance_criteria=[]
            ),
            TaskItem(
                task_id="T2",
                title="Task 2",
                description="Depends on non-existent T99",
                priority="Medium",
                estimated_hours=2.0,
                dependencies=["T99"],
                acceptance_criteria=[]
            ),
        ]
    )

    # Act
    result = validate_task_dependencies(task_plan)

    # Assert
    assert result.is_valid is False
    assert result.missing_dependencies == ["T99"]
    assert len(result.error_messages) == 1
    assert "T99" in result.error_messages[0]


def test_validate_task_dependencies_circular():
    # Arrange: 存在循環依賴 T1 -> T2 -> T3 -> T1
    task_plan = TaskPlan(
        project_name="Circular Dependency Project",
        summary="Project with a cycle between T1, T2, T3",
        tasks=[
            TaskItem(
                task_id="T1",
                title="Task 1",
                description="Depends on T3",
                priority="High",
                estimated_hours=1.0,
                dependencies=["T3"],
                acceptance_criteria=[]
            ),
            TaskItem(
                task_id="T2",
                title="Task 2",
                description="Depends on T1",
                priority="Medium",
                estimated_hours=2.0,
                dependencies=["T1"],
                acceptance_criteria=[]
            ),
            TaskItem(
                task_id="T3",
                title="Task 3",
                description="Depends on T2",
                priority="Low",
                estimated_hours=3.0,
                dependencies=["T2"],
                acceptance_criteria=[]
            ),
        ]
    )

    # Act
    result = validate_task_dependencies(task_plan)

    # Assert
    assert result.is_valid is False
    assert result.has_cycle is True
    assert len(result.cycle_path) > 0
    assert result.cycle_path[0] == result.cycle_path[-1]  # 形成閉環
    assert any("循環依賴" in msg for msg in result.error_messages)


def test_validate_task_dependencies_self_loop():
    # Arrange: T1 自己依賴自己 T1
    task_plan = TaskPlan(
        project_name="Self Loop Project",
        summary="Project where T1 depends on T1",
        tasks=[
            TaskItem(
                task_id="T1",
                title="Task 1",
                description="Self referencing task",
                priority="High",
                estimated_hours=1.0,
                dependencies=["T1"],
                acceptance_criteria=[]
            )
        ]
    )

    # Act
    result = validate_task_dependencies(task_plan)

    # Assert
    assert result.is_valid is False
    assert result.has_cycle is True
    assert result.cycle_path == ["T1", "T1"]
