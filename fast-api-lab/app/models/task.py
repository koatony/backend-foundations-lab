from sqlalchemy import Column, String, DateTime, Text
from app.database import Base
from datetime import datetime, timezone
import uuid

class TaskModel(Base):
    __tablename__ = "tasks"

    # 使用 lambda 確保每一筆新增的資料都會執行新生成 UUID
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    
    priority = Column(String, default="MEDIUM", nullable=False)
    status = Column(String, default="TODO", nullable=False)
    
    # 在 Python 端使用 datetime.now(timezone.utc) 生成標準 UTC 時間
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc), nullable=True)