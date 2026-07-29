from fastapi import APIRouter, status, HTTPException
from app.schemas.item import ItemCreate, ItemResponse
from app.repositories.item_repository import ItemRepository

router = APIRouter(prefix="/items", tags=["items"])
repo = ItemRepository()

@router.post("", status_code = status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    created_item = repo.create(item)
    return created_item


@router.get("", status_code = status.HTTP_200_OK, response_model = list[ItemResponse])
def list_all() -> list[ItemResponse]:
    return repo.list_all()



@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_by_id(item_id: str) -> ItemResponse:
    item = repo.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item    

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(item_id: str) -> None:
    if not repo.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return
