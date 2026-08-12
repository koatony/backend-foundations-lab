from app.repositories.item_repository import ItemRepository
from app.services.ItemService import ItemService
from fastapi import Depends
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


_repo = ItemRepository()


def get_item_repository():
    return _repo


def get_item_service(repo: ItemRepository = Depends(get_item_repository)) -> ItemService:
    return ItemService(item_repo=repo)


_task_repo = TaskRepository()


def get_task_repository():
    return _task_repo


def get_task_service(repo: TaskRepository = Depends(get_task_repository)) -> TaskService:
    return TaskService(task_repo=repo)
