from app.schemas.item import ItemCreate, ItemResponse
from app.repositories.item_repository import ItemRepository
from app.exceptions.exceptions import ItemNotFoundError, DuplicateItemError


class ItemService():
    def __init__(self, item_repo:ItemRepository):
        self.item_repo = item_repo
        
    def create_item(self,item_data:ItemCreate) -> ItemResponse:
        """新增商品，若名稱重複則拋出例外"""
        all_item_list = self.item_repo.list_all()
        for item in all_item_list:
            if item.title.lower() == item_data.title.lower():
                raise DuplicateItemError(
                    f"商品名稱 '{item_data.title}' 已存在於資料庫中"
                )
        return self.item_repo.create(item_data)

    
    def get_by_id(self, item_id:str) -> ItemResponse:
        result = self.item_repo.get_by_id(item_id)
        if not result:
            raise ItemNotFoundError(f"商品ID {item_id} 不存在於資料庫中")
        return result

    def list_all(self) -> list[ItemResponse]:
        return self.item_repo.list_all()

    def delete(self,item_id:str) -> None:
        if not self.item_repo.get_by_id(item_id):
            raise ItemNotFoundError(f"商品ID {item_id} 不存在於資料庫中")
        return self.item_repo.delete(item_id)
    

    
    