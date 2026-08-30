import time
import random
from datetime import datetime, timedelta, timezone
from sqlalchemy import text
from app.database import engine, SessionLocal
from app.models.task import TaskModel

def seed_tasks(total_count=100000):
    print(f"🚀 開始填入 {total_count} 筆 Task 資料至 PostgreSQL...")
    db = SessionLocal()
    try:
        # 清空舊資料
        db.execute(text("TRUNCATE TABLE tasks;"))
        db.commit()

        statuses = ["PENDING", "COMPLETED", "IN_PROGRESS", "TODO"]
        priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        now = datetime.now(timezone.utc)

        batch_size = 10000
        objects = []
        start_time = time.time()

        for i in range(1, total_count + 1):
            # 隨機產生過去 30 天內的時間
            random_days = random.uniform(0, 30)
            created_at = now - timedelta(days=random_days)
            
            task = TaskModel(
                title=f"Benchmark Task {i}",
                description=f"Description for task {i} with some long text to fill disk pages...",
                priority=random.choice(priorities),
                status=random.choice(statuses),
                created_at=created_at
            )
            objects.append(task)

            if len(objects) >= batch_size:
                db.bulk_save_objects(objects)
                db.commit()
                objects.clear()
                print(f"  已塞入 {i} / {total_count} 筆...")

        if objects:
            db.bulk_save_objects(objects)
            db.commit()

        elapsed = time.time() - start_time
        print(f"✅ 完成塞入 {total_count} 筆資料！耗時: {elapsed:.2f} 秒\n")
    finally:
        db.close()

def run_explain(query_sql, description):
    print(f"==================================================")
    print(f"🔍 測試項目：{description}")
    print(f"SQL: {query_sql.strip()}")
    print(f"--------------------------------------------------")
    with engine.connect() as conn:
        result = conn.execute(text(f"EXPLAIN ANALYZE {query_sql}"))
        rows = result.fetchall()
        for row in rows:
            print(row[0])
    print(f"==================================================\n")

def run_benchmark():
    # 1. 確保無索引狀態（刪除舊索引）
    with engine.connect() as conn:
        conn.execute(text("DROP INDEX IF EXISTS idx_status_created;"))
        conn.commit()

    print("--- 🔴 第一階段：未建立複合索引 (無 idx_status_created) ---")
    run_explain(
        "SELECT * FROM tasks WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL '7 days';",
        "1. 雙條件查詢 (未建立索引 -> 預期 Seq Scan 全表掃描)"
    )

    # 2. 建立複合索引 idx_status_created (status, created_at)
    print("⚡ 正在建立複合索引 CREATE INDEX idx_status_created ON tasks(status, created_at)...")
    start_idx = time.time()
    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX idx_status_created ON tasks(status, created_at);"))
        conn.commit()
    print(f"✅ 複合索引建立完成！耗時: {time.time() - start_idx:.2f} 秒\n")

    print("--- 🟢 第二階段：已建立複合索引 (status, created_at) ---")
    
    # 測試 1：遵循最左字首原則 (status + created_at) -> 預期 Index Scan
    run_explain(
        "SELECT * FROM tasks WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL '7 days';",
        "2. 雙條件查詢 (遵循最左字首 -> 預期 Index Scan 命中索引)"
    )

    # 測試 2：違反最左字首原則 (只有 created_at) -> 預期 Seq Scan
    run_explain(
        "SELECT * FROM tasks WHERE created_at > NOW() - INTERVAL '7 days';",
        "3. 單查 created_at (違反最左字首原則 -> 預期 Seq Scan 退化為全表掃描)"
    )

    # 測試 3：Covering Index 覆蓋索引 (只查 SELECT status, created_at) -> 預期 Index Only Scan
    run_explain(
        "SELECT status, created_at FROM tasks WHERE status = 'PENDING' AND created_at > NOW() - INTERVAL '7 days';",
        "4. 覆蓋索引查詢 (SELECT 欄位皆在索引內 -> 預期 Index Only Scan 免回表)"
    )

if __name__ == "__main__":
    seed_tasks(100000)
    run_benchmark()
