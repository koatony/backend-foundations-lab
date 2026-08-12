from typing import Optional, List
from app.schemas.task_plan import TaskPlan, DependencyValidationResult

def validate_task_dependencies(task_plan:TaskPlan) -> DependencyValidationResult:
    """
    核心驗證邏輯，將 Week 2 建立的邏輯抽象為獨立工具函式。
    檢查以下四點：
    1. 格式正確性（由 Pydantic 處理，此處不重複檢查）。
    2. 任務 ID 不重複。
    3. 依賴關係無循環（DAG）。
    4. 依賴的 Task ID 是否存在。
    """
    all_tasks = {t.task_id for t in task_plan.tasks}

    # 1. 檢查Task ID 重複
    if len(all_tasks) != len(task_plan.tasks):
        return DependencyValidationResult(
            is_valid=False,
            error_messages=["任務 ID 不能重複，請檢查是否有重複的 task_id。"],
            missing_dependencies=[],
            has_cycle=False,
            cycle_path = []
        )

    # 2. 檢查依賴的 Task ID 是否存在
    missing_deps = []
    for t in task_plan.tasks:
        for dep in t.dependencies:
            if dep not in all_tasks:
                missing_deps.append(dep)
                
    if missing_deps:
        # 去除重複項
        missing_deps = list(set(missing_deps))
        return DependencyValidationResult(
            is_valid=False,
            error_messages=[f"以下相依的 Task ID 不存在: {', '.join(missing_deps)}"],
            missing_dependencies=missing_deps,
            has_cycle=False,
            cycle_path=[]
        )

    # 3. 檢查循環依賴
    graph = {t.task_id: t.dependencies for t in task_plan.tasks}

    # {id: 'visiting'|'finished'}
    visited = {}

    for task_id in sorted(all_tasks):
        # 如果已經處理過，則跳過
        if visited.get(task_id) != "finished":
            path = []
            cycle = has_cycle(task_id, graph, visited, path)
            if cycle is not None:
                return DependencyValidationResult(
                    is_valid = False,
                    error_messages = [f"任務之間存在循環依賴: {' -> '.join(cycle)}"],
                    missing_dependencies=[],
                    has_cycle=True,
                    cycle_path=cycle
                )
    

    return DependencyValidationResult(is_valid=True)
    


def has_cycle(task_id:str, graph:dict, visited:dict, path: list) -> Optional[List[str]]:
    """
    DFS 偵測循環依賴。
    如果偵測到循環，回傳完整的循環路徑（例如 ['T1', 'T2', 'T3', 'T1']）；
    若無循環，則回傳 None。
    """
    if visited.get(task_id) == 'visiting':
        # 找到循環！從 path 中擷取出循環起點到終點的路徑，並加上當前節點閉合路徑
        start_idx = path.index(task_id)
        return path[start_idx:] + [task_id]
        
    if visited.get(task_id) == 'finished':
        return None
    
    visited[task_id] = 'visiting'
    path.append(task_id)

    for neighbor in graph.get(task_id, []):
        cycle_path = has_cycle(neighbor, graph, visited, path)
        if cycle_path is not None:
            return cycle_path

    visited[task_id] = 'finished'
    path.pop() # 回溯時移除
    return None