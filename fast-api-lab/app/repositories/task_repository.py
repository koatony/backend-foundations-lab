import uuid
from dataclasses import dataclass, field
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from datetime import datetime, timezone
from typing import Optional
from app.database import get_db
from app.models import TaskModel
from sqlalchemy.orm import Session


def _to_TaskResponse(tm:TaskModel) -> TaskResponse:
    return TaskResponse(
        id = tm.id,
        created_at = tm.created_at,
        priority = tm.priority,
        description = tm.description,
        status = tm.status,
        updated_at = tm.updated_at,
        title = tm.title
    )






@dataclass
class TaskRepository:
    # _storage: dict[str, TaskResponse] = field(default_factory=dict)
    
    def __init__(self, db:Session): 
        self.db = db   

    def create(self, task: TaskCreate) -> TaskResponse:
        
        task_model = TaskModel(
            title = task.title,
            description = task.description,
            priority = task.priority
        )

        self.db.add(task_model)
        self.db.commit()
        self.db.refresh(task_model)
        

        
        response = _to_TaskResponse(task_model)

        return response
        

    def update(self, task_id: str, task_input: TaskUpdate) -> Optional[TaskResponse]:
        target = self.db.query(TaskModel).filter(TaskModel.id==task_id).first()
        if target is None:
            return None
        

        
        
        update_dict = task_input.model_dump()

        for key, value in update_dict.items():
            if value is not None:
                setattr(target, key, value)
        target.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(target)
        
        

        return _to_TaskResponse(target)

    def get_by_id(self, task_id: str) -> Optional[TaskResponse]:
        target = self.db.query(TaskModel).filter(TaskModel.id==task_id).first()
        if target is None:
            return None
        return _to_TaskResponse(target)

    def list_all(self) -> list[TaskResponse]:
        target = self.db.query(TaskModel).all()
        return [_to_TaskResponse(t) for t in target]

    def delete(self, task_id: str) -> bool:
        target = self.db.query(TaskModel).filter(TaskModel.id==task_id).first()
        if target is None:
            return False
        self.db.delete(target)
        self.db.commit()
        return True
        
