from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.exceptions.exceptions import TaskNotFoundError


class TaskService():
    def __init__(self,task_repo:TaskRepository):
        self.task_repo = task_repo



    def create_task(self, task:TaskCreate) -> TaskResponse:
        return self.task_repo.create(task)

    def list_tasks(self,skip:int= 0, limit:int = 10,status:str | None = None)->list[TaskResponse]:
        return self.task_repo.list_all(skip=skip, limit=limit, status=status)


    def update_task(self, task_id:str, task_input:TaskUpdate)->TaskResponse:
        result = self.task_repo.update(task_id, task_input)
        if not result:
            raise TaskNotFoundError(task_id)
        return result

    def delete_task(self, task_id:str)->bool:
        if not self.task_repo.get_by_id(task_id):
            raise TaskNotFoundError(task_id)
        return self.task_repo.delete(task_id)

    def get_by_id(self,task_id:str) -> TaskResponse:
        result = self.task_repo.get_by_id(task_id)
        if not result:
            raise TaskNotFoundError(task_id)
        return result
    

    
