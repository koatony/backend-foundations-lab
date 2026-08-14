from pydantic import BaseModel
from typing import Literal
from datetime import datetime



# 前端給我得資料
class TaskCreate(BaseModel):
    title:str
    description:str | None
    priority: Literal["LOW","MEDIUM","HIGH"]


# 更新時不用填寫完整
class TaskUpdate(BaseModel):
    title:str | None = None
    description: str | None = None
    priority : Literal["LOW","MEDIUM","HIGH"] | None = None
    status : Literal["TODO","IN_PROGRESS","DONE"] | None = None

# 回傳給前端的資料
class TaskResponse(BaseModel):
    title:str
    description: str | None
    priority: Literal["LOW","MEDIUM","HIGH"]
    status: Literal["TODO","IN_PROGRESS","DONE"]
    id:str
    created_at: datetime
    updated_at: datetime | None

