from fastapi import APIRouter, Depends, status, Response
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.dependencies import get_task_service
from fastapi import Query
from typing import Optional

router = APIRouter(prefix="/tasks",tags=["tasks"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(task:TaskCreate, task_service:TaskService=Depends(get_task_service)):
    return task_service.create_task(task)


@router.get("", status_code=status.HTTP_200_OK, response_model = list[TaskResponse])
def list_all(
        skip:int = Query(0, ge=0),
        limit:int = Query(10, ge=0),
        status:Optional[str] = None,
        task_service:TaskService=Depends(get_task_service)
    ):
    return task_service.list_tasks(skip, limit, status)


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def get_by_id(task_id: str,task_service:TaskService=Depends(get_task_service)) -> TaskResponse:
    return task_service.get_by_id(task_id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete(task_id: str,task_service:TaskService=Depends(get_task_service)):
    task_service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponse)
def update(task_id: str, task_input:TaskUpdate,task_service:TaskService=Depends(get_task_service)) -> TaskResponse:
    return task_service.update_task(task_id, task_input)