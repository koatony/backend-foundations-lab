from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal


# 單一任務物件
class TaskItem(BaseModel):
    task_id: str
    title: str
    description: str
    priority: Literal["High", "Medium", "Low"] = Field(..., description="任務優先級，僅能選擇 High, Medium, Low")
    estimated_hours: float = Field(..., gt=0, description="任務預計所需工時")
    dependencies: List[str] = Field(default_factory=list, description="前置任務ID列表")
    acceptance_criteria: List[str] = Field(default_factory=list, description="驗收列表 可為空")


# 完整計畫
class TaskPlan(BaseModel):
    project_name: str
    summary: str
    tasks: List[TaskItem]


# 驗證結果容器
class TaskPlanValidationResult(BaseModel):
    """
    用來記錄每次 Validation 的成功/失敗狀態，方便後續 Log 與 Week 3 Retry 機制使用。
    """
    is_valid: bool
    data: Optional[TaskPlan] = None
    raw_response: str
    error_message: Optional[str] = None
    validation_errors: Optional[List[dict]] = None


# 裝驗證結果
class DependencyValidationResult(BaseModel):
    is_valid: bool
    missing_dependencies: List[str] = Field(default_factory=list, description="不存在的 Task ID 列表")
    has_cycle: bool = False
    cycle_path: List[str] = Field(default_factory=list, description="偵測到的循環路徑，例如 ['T1', 'T2', 'T3', 'T1']")
    error_messages: List[str] = Field(default_factory=list, description="人類可讀的錯誤描述，方便當作 Prompt 反饋給 LLM")


def validate_task_dependencies(task_plan: TaskPlan) -> DependencyValidationResult:
    all_tasks = {t.task_id for t in task_plan.tasks}
    missing_deps = []
    error_messages = []

    # 1. 檢查是否存在未定義的 task_id (missing dependencies)
    for task in task_plan.tasks:
        for dep in task.dependencies:
            if dep not in all_tasks:
                missing_deps.append(dep)
                error_messages.append(f"任務 '{task.task_id}' 依賴了不存在的任務 ID: '{dep}'")

    # 去重 missing_deps (保留順序)
    missing_deps = list(dict.fromkeys(missing_deps))

    # 2. 建立圖 (Graph) 並用 DFS 檢查循環依賴
    graph = {t.task_id: t.dependencies for t in task_plan.tasks}
    visited = {}
    cycle_path = []

    def dfs(task_id: str, current_path: list) -> bool:
        visited[task_id] = "visiting"
        current_path.append(task_id)

        for neighbor in graph.get(task_id, []):
            if neighbor not in graph:
                continue
            if visited.get(neighbor) == "visiting":
                idx = current_path.index(neighbor)
                cycle_path.extend(current_path[idx:] + [neighbor])
                return True
            if visited.get(neighbor) != "finished":
                if dfs(neighbor, current_path):
                    return True

        current_path.pop()
        visited[task_id] = "finished"
        return False

    has_cycle = False
    for task_id in sorted(all_tasks):
        if visited.get(task_id) != "finished":
            if dfs(task_id, []):
                has_cycle = True
                cycle_str = " -> ".join(cycle_path)
                error_messages.append(f"任務之間存在循環依賴: {cycle_str}")
                break

    is_valid = (len(missing_deps) == 0) and (not has_cycle)

    return DependencyValidationResult(
        is_valid=is_valid,
        missing_dependencies=missing_deps,
        has_cycle=has_cycle,
        cycle_path=cycle_path,
        error_messages=error_messages
    )
