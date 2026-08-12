import pytest
from unittest.mock import patch, MagicMock
from app.agent.task_plan_agent import (
    validate_and_parse_json,
    generate_feedback_prompt,
    generate_task_plan_with_retry,
)
from app.schemas.task_plan import TaskPlanValidationResult, TaskPlan


# 1. 測試 validate_and_parse_json - 成功案例
def test_validate_and_parse_json_success():
    # Arrange
    raw_json = """{
        "project_name": "Sony Camera Buying Guide",
        "summary": "Full focal length camera setup for 2026",
        "tasks": [
            {
                "task_id": "T1",
                "title": "Select Body",
                "description": "Choose flagship full-frame body",
                "priority": "High",
                "estimated_hours": 2.0,
                "dependencies": [],
                "acceptance_criteria": ["Body identified"]
            }
        ]
    }"""

    # Act
    result = validate_and_parse_json(raw_json)

    # Assert
    assert result.is_valid is True
    assert isinstance(result.data, TaskPlan)
    assert result.data.project_name == "Sony Camera Buying Guide"
    assert len(result.data.tasks) == 1
    assert result.data.tasks[0].priority == "High"
    assert result.validation_errors == []


# 2. 測試 validate_and_parse_json - Pydantic ValidationError 案例
def test_validate_and_parse_json_pydantic_error():
    # Arrange: priority 不符合 High/Medium/Low, estimated_hours <= 0
    invalid_pydantic_json = """{
        "project_name": "Sony Camera Buying Guide",
        "summary": "Invalid priority test",
        "tasks": [
            {
                "task_id": "T1",
                "title": "Select Body",
                "description": "Invalid priority value",
                "priority": "Ultra High",
                "estimated_hours": -1.0,
                "dependencies": [],
                "acceptance_criteria": []
            }
        ]
    }"""

    # Act
    result = validate_and_parse_json(invalid_pydantic_json)

    # Assert
    assert result.is_valid is False
    assert result.data is None
    assert "Pydantic 驗證失敗" in result.error_message
    assert result.validation_errors is not None
    assert len(result.validation_errors) >= 2  # priority and estimated_hours errors


# 3. 測試 validate_and_parse_json - 非法 JSON 格式案例
def test_validate_and_parse_json_invalid_json_format():
    # Arrange
    bad_json = "{ this is not valid json }"

    # Act
    result = validate_and_parse_json(bad_json)

    # Assert
    assert result.is_valid is False
    assert result.data is None
    assert "JSON無法解析" in result.error_message or "Pydantic 驗證失敗" in result.error_message


# 4. 測試 generate_feedback_prompt - 驗證錯誤格式轉換
def test_generate_feedback_prompt():
    # Arrange
    validation_result = TaskPlanValidationResult(
        is_valid=False,
        raw_response="{}",
        error_message="Validation Failed",
        validation_errors=[
            {
                "loc": ("tasks", 0, "priority"),
                "msg": "Input should be 'High', 'Medium' or 'Low'",
                "type": "enum",
            },
            {
                "loc": ("tasks", 0, "estimated_hours"),
                "msg": "Input should be greater than 0",
                "type": "greater_than",
            },
        ],
    )

    # Act
    feedback = generate_feedback_prompt(validation_result)

    # Assert
    assert "請根據以下錯誤修正" in feedback
    assert '在 "tasks -> 0 -> priority" 發生錯誤' in feedback
    assert '在 "tasks -> 0 -> estimated_hours" 發生錯誤' in feedback


# 5. 測試 generate_task_plan_with_retry - 第一次即成功 (Pass@1)
@patch("app.agent.task_plan_agent.llm_client.generate")
def test_retry_loop_success_first_try(mock_generate):
    # Arrange
    valid_json = """{
        "project_name": "Test Project",
        "summary": "Summary",
        "tasks": [
            {
                "task_id": "T1",
                "title": "Task 1",
                "description": "Desc 1",
                "priority": "High",
                "estimated_hours": 1.5,
                "dependencies": [],
                "acceptance_criteria": []
            }
        ]
    }"""
    mock_generate.return_value = valid_json

    # Act
    result = generate_task_plan_with_retry("請建立一個任務計畫", max_retres=3)

    # Assert
    assert result.is_valid is True
    assert mock_generate.call_count == 1
    assert result.data.project_name == "Test Project"


# 6. 測試 generate_task_plan_with_retry - 第一次失敗，第二次修正成功
@patch("app.agent.task_plan_agent.llm_client.generate")
def test_retry_loop_success_after_retry(mock_generate):
    # Arrange
    invalid_json = """{
        "project_name": "Test Project",
        "summary": "Summary",
        "tasks": [
            {
                "task_id": "T1",
                "title": "Task 1",
                "description": "Desc 1",
                "priority": "InvalidPriority",
                "estimated_hours": 1.5,
                "dependencies": [],
                "acceptance_criteria": []
            }
        ]
    }"""
    valid_json = """{
        "project_name": "Test Project Fixed",
        "summary": "Summary",
        "tasks": [
            {
                "task_id": "T1",
                "title": "Task 1",
                "description": "Desc 1",
                "priority": "High",
                "estimated_hours": 1.5,
                "dependencies": [],
                "acceptance_criteria": []
            }
        ]
    }"""

    mock_generate.side_effect = [invalid_json, valid_json]

    # Act
    result = generate_task_plan_with_retry("請建立一個任務計畫", max_retres=3)

    # Assert
    assert result.is_valid is True
    assert mock_generate.call_count == 2
    assert result.data.project_name == "Test Project Fixed"

    # 驗證第二次被呼叫的 prompt 是否包含反饋訊息
    second_call_prompt = mock_generate.call_args_list[1][0][1]
    assert "【請修正以下錯誤】" in second_call_prompt
    assert "tasks -> 0 -> priority" in second_call_prompt


# 7. 測試 generate_task_plan_with_retry - 超過最大重試次數 (Exceed Max Retries)
@patch("app.agent.task_plan_agent.llm_client.generate")
def test_retry_loop_exceed_max_retries(mock_generate):
    # Arrange
    invalid_json = """{
        "project_name": "Test Project",
        "summary": "Summary",
        "tasks": []
    }"""
    # 讓 LLM 一直回傳缺欄位的無效 JSON
    mock_generate.return_value = "{ invalid json }"

    # Act
    result = generate_task_plan_with_retry("請建立一個任務計畫", max_retres=3)

    # Assert
    assert result.is_valid is False
    assert mock_generate.call_count == 3
    assert "JSON無法解析" in result.error_message or "Pydantic 驗證失敗" in result.error_message
