import uuid
from datetime import datetime
from app.schemas.item import ItemResponse,ItemCreate
from dataclasses import dataclass, field
from typing import Optional
@dataclass
class ItemRepository:
    storage:dict[str, ItemResponse] = field(default_factory = dict)


    def create(self, item:ItemCreate) -> ItemResponse:
        item_id = str(uuid.uuid4())
        created_at = datetime.now()

        response = ItemResponse(id = item_id, created_at = created_at, **item.model_dump()) 
        self.storage[item_id] = response

        return response    
    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        if item_id not in self.storage:
            return None
        else:
            return self.storage[item_id]
        
    def list_all(self) -> list[ItemResponse]:
        return list(self.storage.values())  

    def delete(self, item_id:str)->bool:
        if item_id not in self.storage:
            return False
        else:
            del self.storage[item_id]
            return True

    