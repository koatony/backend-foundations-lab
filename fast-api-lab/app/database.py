from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import Generator
from app.core import settings

# 1. 建立基本連線參數
engine_args = {
    "pool_pre_ping": True  # 每次使用連線前先 ping，避免使用到已斷開的連線
}

# 2. 依據資料庫種類動態配置
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite 專屬設定，關閉跨執行緒檢查限制
    engine_args["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL / MySQL 支援的連線池設定
    engine_args["pool_size"] = 10
    engine_args["max_overflow"] = 20
    engine_args["pool_timeout"] = 30
    engine_args["pool_recycle"] = 1800

# 3. 建立連線引擎 (Engine)
engine = create_engine(settings.DATABASE_URL, **engine_args)

# 4. 建立 Session 工廠
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. 建立宣告基底 (Base)，用於 ORM Models 繼承
Base = declarative_base()


# 6. 宣告 Dependency Injection 使用的 DB 生成器
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI 依賴注入使用 (Depends)：
    為每個 Request 建立獨立的 DB Session，並在 Request 結束後自動 close (yield 模式)。
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
