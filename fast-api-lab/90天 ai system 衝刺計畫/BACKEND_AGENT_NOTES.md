# 90天 AI System 衝刺計畫 — Backend & Agent 學習筆記本

本筆記本用於紀錄 **Backend Foundations** 與 **Agent Loop Engineering** 的核心觀念、架構設計、最佳實踐與實務踩坑經驗。

---

## 📅 2026-08-14 學習日誌：ORM、Alembic、FastAPI 依賴注入與測試實戰

今天針對資料庫遷移、SQLAlchemy ORM 運轉機制、FastAPI 依賴注入與資料庫單元/整合測試進行了深度的觀念拆解與實作。以下為今天學到的重點觀念與應用位置：

---

### 1. Alembic 與資料庫動態配置
* **學到了什麼**：
  * `sqlalchemy.url` 是資料庫的門牌號碼（Connection String）。
  * 在 `env.py` 中寫入 `config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)`，可以使用 Pydantic Settings 從環境變數動態取代 `alembic.ini` 中的網址。
* **用在哪裡**：
  * 當要在本地端 SQLite 測試與部署 PostgreSQL 之間切換時，直接前綴 `DATABASE_URL="sqlite:///./dev.db" alembic upgrade head` 即可，不用改動任何專案程式碼。

---

### 2. SQLAlchemy ORM 運作與 DTO 防火牆
* **學到了什麼**：
  * **Class vs. Instance**：`db.query(TaskModel)` 傳入的是類別（Class，代表整張 Table）；而 `db.add(task_obj)` 傳入的是物件實例（Instance，代表一筆 Row）。
  * **不需要手寫 `__init__`**：繼承 `Base` 後，SQLAlchemy 自動提供欄位建構子，且在 `commit()` 時會自動觸發 `default`（如 UUID、預設狀態）。
  * **自動髒資料追蹤 (Dirty Tracking)**：從資料庫撈出的持久化物件，直接修改屬性後 `commit()`，SQLAlchemy 會自動根據 Primary Key (PK) 生成 `UPDATE` SQL 指令寫回，不需要呼叫 `db.update()`。
  * **為什麼要 TaskModel ➡️ TaskResponse 轉換**：作為「防火牆（解耦）」。防止資料庫結構改變影響到前端 API 介面，並可過濾敏感欄位。
* **用在哪裡**：
  * `app/repositories/task_repository.py` 內部實作所有 CRUD 與 `_to_TaskResponse` 轉換器。

---

### 3. FastAPI 依賴注入與 `app.dependency_overrides`
* **學到了什麼**：
  * **`Depends` 運作原理**：在 Router 參數宣告 `Depends(func)`，FastAPI 在收到 HTTP 請求時會自動呼叫該函數並注入回傳值。
  * **`app` 物件與 `dependency_overrides`**：`app` 是整個伺服器的大管家。`app.dependency_overrides` 是一個字典，可在測試期間攔截 `Depends(...)`，把實體連線偷天換日成測試專用的連線，而完全不需修改主程式。
  * **`TestClient`**：在記憶體中模擬 HTTP 請求傳給 `app`，不需啟動真實 Uvicorn 伺服器，速度為毫秒級。
* **用在哪裡**：
  * `tests/tasks_api/test_tasks_api.py` 的 client fixture 裡寫 `app.dependency_overrides[get_db] = lambda: db_session`。

---

### 4. SQLite 記憶體測試 (`sqlite:///:memory:`) 與 `StaticPool`
* **學到了什麼**：
  * **`sqlite:///:memory:` 踩坑**：SQLite 記憶體資料庫的生命週期與實體連線綁定。一般連線池每次叫用時若開啟新連線，會連接到「空的記憶體空間」，導致 `OperationalError: no such table`。
  * **`StaticPool`**：強制 Engine 在測試期間永遠只維持唯一一個實體連線。
  * **`check_same_thread=False`**：允許 FastAPI TestClient 跨執行緒調用連線。
* **用在哪裡**：
  * `tests/repositories/test_task_repositoy_db.py` 與 `tests/tasks_api/test_tasks_api.py` 的 `db_session` fixture 建立 `create_engine` 時。

---

### 5. 函數呼叫避坑：關鍵字參數 (Keyword Arguments)
* **學到了什麼**：
  * 呼叫包含多個選擇性參數的方法時，若使用位置傳參（Positional），順序對不上會導致參數調包（如 `skip` 傳給 `limit`，導致 `limit=0` 撈回空清單 `[]`）。
  * 永遠使用指名道姓的關鍵字傳參：`self.task_repo.list_all(limit=limit, skip=skip, status=status)`。
* **用在哪裡**：
  * `app/services/task_service.py` 轉傳參數至 Repository 時。

---

> 📝 *後續新的重點筆記將持續補充於此處。*
