import pytest
from app.repositories.item_repository import ItemRepository
from app.services.ItemService import ItemService
from app.schemas.item import ItemCreate, ItemResponse
from app.exceptions.exceptions import ItemNotFoundError, DuplicateItemError
from unittest.mock import MagicMock
from datetime import datetime, timezone


@pytest.fixture
def mock_repo():
    # 建造假的ItemRepository用來測試
    mock = MagicMock()
    return mock

@pytest.fixture
def item_service(mock_repo):
    # 建造ItemService並注入假的ItemRepository
    return ItemService(item_repo=mock_repo)



# ---------------------------------------------------------
# 1. 測試建立商品成功
# ---------------------------------------------------------
def test_create_item_success(item_service, mock_repo):
    # 準備測試資料
    mock_repo.list_all.return_value = []

    mock_item = ItemResponse(
        id = "item-1",
        title = "test item",
        description = "test desc",
        price = 100.0,
        created_at = datetime.now(timezone.utc)
    )

    mock_repo.create.return_value = mock_item

    # 執行
    item_data = ItemCreate(
        title = "test item",
        description = "test desc",
        price = 100.0
    )

    result = item_service.create_item(item_data)

    # 断言
    assert result.title == "test item"
    assert result.price == 100.0

    mock_repo.create.assert_called_once_with(item_data)
        
    

def test_create_item_duplicate_title_raises_error(item_service,mock_repo):
    
    # 準備測試資料

    existing_item = ItemResponse(
        id = "item-1",
        title = "test item",
        description = "test desc",
        price = 100.0,
        created_at = datetime.now(timezone.utc)
    )
    mock_repo.list_all.return_value = [existing_item]

    # 執行
    item_data = ItemCreate(
        title = "test item",
        description = "test desc",
        price = 100.0
    )

    with pytest.raises(DuplicateItemError):
        item_service.create_item(item_data)



def test_get_by_id_not_found_raises_error(item_service, mock_repo):
    # 建立測試資料
    mock_repo.get_by_id.return_value = None

    # 執行
    with pytest.raises(ItemNotFoundError):
        item_service.get_by_id("non-existent-id")


def test_delete_not_found_raises_error(item_service, mock_repo):

    #建立測試資料
    mock_repo.get_by_id.return_value = None


    # 執行
    with pytest.raises(ItemNotFoundError):
        item_service.delete("non-existent-id")


