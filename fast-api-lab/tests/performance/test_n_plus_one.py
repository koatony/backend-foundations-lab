import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, selectinload, joinedload
from app.database import Base
from app.models.user import UserModel
from app.models.task import TaskModel



@pytest.fixture
def db_session_with_counter():
    """
    建立測試記憶體 DB，並注入 SQL 計數監聽器 (event.listens_for)。
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    query_count = 0

    # 利用 SQLAlchemy Event 監聽器，每當發送 SQL 到 DB 時，計數器 +1
    @event.listens_for(engine, "before_cursor_execute")
    def count_queries(conn, cursor, statement, parameters, context, executemany):
        nonlocal query_count
        query_count += 1

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # 預先寫入 50 位 User，每位 User 配 2 個 Task
    for i in range(50):
        user = UserModel(name=f"User_{i}", email=f"user_{i}@example.com")
        user.tasks = [
            TaskModel(title=f"Task_{i}_1"),
            TaskModel(title=f"Task_{i}_2"),
        ]
        session.add(user)

    session.commit()
    session.expunge_all()  # 清空 Session 快取，確保之後的查詢都是真正對 DB 下 SQL

    # 重置計數器，排除掉初始化塞資料的 SQL 次數
    query_count = 0

    def get_query_count():
        return query_count

    def reset_query_count():
        nonlocal query_count
        query_count = 0

    yield session, get_query_count, reset_query_count

    session.close()


def test_reproduce_n_plus_one_disaster(db_session_with_counter):
    """
    【階段二驗證】重現 N+1 災難：Lazy Loading 導致發送 1 + 50 = 51 次 SQL 查詢
    """
    session, get_query_count, reset_query_count = db_session_with_counter

    # 1. 撈出 50 個 User (觸發第 1 次 SQL: SELECT * FROM users)
    # users = session.query(UserModel).all()
    users = session.query(UserModel).options(selectinload(UserModel.tasks)).all()

    for user in users:
        _ = [task.title for task in user.tasks]



    # # 2. 遍歷每位 User 存取 user.tasks (觸發 50 次子查詢: SELECT * FROM tasks WHERE user_id = ?)
    # all_task_titles = []
    # for user in users:
    #     titles = [task.title for task in user.tasks]
    #     all_task_titles.append(titles)

    # 精準斷言：1 次主查詢 + 50 次子查詢 = 51 次 SQL！
    total_sqls = get_query_count()
    print(f"\n[Lazy Loading 災難測試] 處理 50 位 User，總共發送了 {total_sqls} 次 SQL 查詢！")
    # assert total_sqls == 51, f"預期發送 51 次 SQL，實際發送了 {total_sqls} 次"
    # assert len(all_task_titles) == 50

    assert total_sqls == 2