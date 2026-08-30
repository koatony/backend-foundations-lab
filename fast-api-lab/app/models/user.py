from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone
import uuid


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    # 1對多關係：一個 User 有多個 Task
    tasks = relationship("TaskModel", back_populates="user")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
