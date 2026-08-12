import uuid
from dataclasses import dataclass, field
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime, timezone
from typing import Optional


@dataclass
class TaskRepository:
    _storage: dict[str, TaskResponse] = field(default_factory=dict)

    def create(self, task: TaskCreate) -> TaskResponse:
        task_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)
        status = "TODO"
        updated_at = datetime.now(timezone.utc)
        response = TaskResponse(id=task_id, created_at=created_at, status=status, updated_at=updated_at, **task.model_dump())
        self._storage[task_id] = response
        return response

    def update(self, task_id: str, task_input: TaskUpdate) -> Optional[TaskResponse]:
        if task_id not in self._storage:
            return None

        existing_task = self._storage[task_id]
        update_dict = task_input.model_dump()

        for key, value in update_dict.items():
            if value is not None:
                setattr(existing_task, key, value)

        existing_task.updated_at = datetime.now(timezone.utc)
        self._storage[task_id] = existing_task
        return existing_task

    def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        return self._storage.get(task_id)

    def list_all(self) -> list[TaskResponse]:
        return list(self._storage.values())

    def delete(self, task_id: str) -> bool:
        return self._storage.pop(task_id, None) is not None
