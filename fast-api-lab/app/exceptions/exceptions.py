class ItemNotFoundError(Exception):
    """商品不存在時拋出"""
    pass

class DuplicateItemError(Exception):
    """商品名稱重複時拋出"""
    pass


class TaskNotFoundError(Exception):
    """任務不存在時拋出"""
    def __init__(self, task_id: str, message: str = "不存在於資料庫中"):
        self.task_id = task_id
        self.message = f"任務ID {task_id} {message}"
        super().__init__(self.message)


