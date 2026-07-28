from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
class ItemBase(BaseModel):
    title:str=Field(..., min_length = 1, max_length = 50, title = "商品標題")
    description:Optional[str]=None
    price:float = Field(..., gt=0, title = "商品價格")

    

    
class ItemCreate(ItemBase):
    @field_validator("title")
    @classmethod
    def title_validate(cls, v:str)-> str:
        stripped_value = v.strip()
        if len(stripped_value) == 0:
            raise ValueError("title cannot be empty or whitespace only")
        return stripped_value
    


class ItemResponse(ItemBase):
    id:str
    created_at:datetime


