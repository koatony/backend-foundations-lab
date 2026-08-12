from fastapi import APIRouter, status, HTTPException, Depends, Response
from app.schemas.item import ItemCreate, ItemResponse
from app.services.ItemService import ItemService
from app.dependencies import get_item_service
router = APIRouter(prefix="/items", tags=["items"])

@router.post("", status_code = status.HTTP_201_CREATED)
def create_item(item: ItemCreate,service: ItemService = Depends(get_item_service)):
    return service.create_item(item)


@router.get("", status_code = status.HTTP_200_OK, response_model = list[ItemResponse])
def list_all(service:ItemService = Depends(get_item_service)) -> list[ItemResponse]:
    return service.list_all()



@router.get("/{item_id}", status_code=status.HTTP_200_OK, response_model=ItemResponse)
def get_by_id(item_id: str,service:ItemService = Depends(get_item_service)) -> ItemResponse:
    return service.get_by_id(item_id)    

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete(item_id: str,service:ItemService = Depends(get_item_service)):
    service.delete(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
