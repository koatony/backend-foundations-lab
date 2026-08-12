import uuid
from datetime import datetime, timezone
from app.schemas.item import ItemResponse,ItemCreate
from dataclasses import dataclass, field
from typing import Optional
@dataclass
class ItemRepository:
    _storage:dict[str, ItemResponse] = field(default_factory = dict)

    def create(self, item:ItemCreate) -> ItemResponse:
        item_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc)

        response = ItemResponse(id = item_id, created_at = created_at, **item.model_dump()) 
        self._storage[item_id] = response

        return response    
    def get_by_id(self, item_id: str) -> Optional[ItemResponse]:
        return self._storage.get(item_id)
        
    def list_all(self) -> list[ItemResponse]:
        return list(self._storage.values())  

    def delete(self, item_id:str)->bool:
        return self._storage.pop(item_id, None) is not None

    