import pytest
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate

def test_create_item():
    item = ItemCreate(title = "test",price = 10)
    repo = ItemRepository()
    result = repo.create(item)
    #是否產生id
    assert len(repo._storage) == 1
    assert result.title == "test"
    assert result.price == 10
    assert result == repo._storage.get(result.id)
    
    
@pytest.mark.parametrize("title,price", [
    ("test",10),
    ("test2",20),
    ("test3",30)
])
def test_create_item_id_is_str(title:str, price:int):
    item = ItemCreate(title = title,price = price)
    repo = ItemRepository()
    item_id = repo.create(item).id
    assert len(item_id)>0
    assert isinstance(item_id,str)



    









