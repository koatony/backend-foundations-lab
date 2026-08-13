# 90天 AI System 衝刺計畫 — 練習與作業追蹤表 (EXERCISES.md)

本檔案記錄所有出過的練習題目、交付物路徑與完成狀態，方便自我進度管理與複習。

---

## 📊 練習進度總覽

| 編號 | 練習名稱 | 對應週次 | 主要交付物路徑 | 狀態 | 核心技術點 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ex-01** | Python 基礎與 Exception Handling | W1 | `module-import-lab/app/log_utils.py` <br> `module-import-lab/app/bank_utils.py` | ✅ 已完成 | Context Manager, Exception Bubbling, Keyword-only args |
| **Ex-02** | 手寫 JSON Validator 與 Unit Test | W1 | `module-import-lab/app/json_validator.py` <br> `module-import-lab/tests/test_json_validator.py` | ✅ 已完成 | 手寫型別/必填檢查, 自訂 Exception, pytest parameterize |
| **Ex-03** | TaskPlan Schema & Tool Parser | W2 | `fast-api-lab/app/schemas/task_plan.py` <br> `fast-api-lab/app/agent/tool_parser.py` | ✅ 已完成 | Pydantic BaseModel, Field 限制, inspect 解析函數轉 JSON Schema |
| **Ex-04** | TaskPlan Agent Loop (Generate → Validate → Feedback → Retry) | W2-W4 | `fast-api-lab/app/agent/task_plan_agent.py` <br> `fast-api-lab/tests/agent/test_task_plan_agent.py` | ✅ 已完成 | Pydantic JSON 驗證, ValidationError 提取, Feedback Prompt 產生, 重試迴圈, `@patch` Mock LLM 測試 (7/7 通過) |
| **Ex-05** | 三層架構重構 (Service Layer, Domain Exceptions & Mock 測試) | W3 | `fast-api-lab/app/services/ItemService.py` <br> `fast-api-lab/app/dependencies.py` <br> `fast-api-lab/tests/services/test_item_service.py` | ✅ 已完成 | Router-Service-Repo 三層架構解耦, 自訂 Domain Exceptions, MagicMock 隔離測試, 依賴注入 (Depends) |
| **Ex-06** | Task REST API v0.1 & pytest 完整測試 suite | W4 (Month 1 Gate) | `fast-api-lab/app/schemas/task.py` <br> `fast-api-lab/app/repositories/task_repository.py` <br> `fast-api-lab/app/services/task_service.py` <br> `fast-api-lab/app/routers/tasks.py` <br> `fast-api-lab/tests/services/test_task_service.py` <br> `fast-api-lab/tests/tasks_api/test_tasks_api.py` | ✅ 已完成 | Task CRUD 完整三層 Clean Architecture、Depends 依賴覆寫 (dependency_overrides)、Fixture 作用域、TestClient 整合測試 (25/25 通過) |
| **Ex-07** | Task Dependencies 有向圖 (DAG) 與循環依賴驗證 | W7 | `fast-api-lab/app/schemas/task_plan.py` <br> `fast-api-lab/tests/agent/test_task_plan_validation.py` | ✅ 已完成 | 有向圖 (DAG) 建立, 不存在依賴 ID 檢查, DFS 循環依賴偵測與 cycle_path 提取, pytest 單元測試 (40/40 通過) |
| **Ex-08** | PostgreSQL / SQLAlchemy ORM 與 Alembic 資料庫遷移 | W5-W6 | `fast-api-lab/app/database.py` <br> `fast-api-lab/app/model/task.py` <br> `fast-api-lab/alembic/` <br> `fast-api-lab/app/repositories/task_repository.py` <br> `fast-api-lab/tests/repositories/test_task_repository_db.py` | ⏳ 進行中 (已投入 1.0 h) | PostgreSQL DATABASE_URL 配置, SQLAlchemy ORM Mapping (`TaskModel`), Alembic autogenerate 遷移腳本, TaskRepository 連線 Session 管理, SQLite In-Memory DB 測試 |

---

## 📝 練習詳細規格記錄

### 【Ex-04】TaskPlan Agent Loop (Generate → Validate → Feedback → Retry)
- **完成時間**：2026-08-05
- **要求說明**：
  1. **`validate_and_parse_json(raw_json: str) -> TaskPlanValidationResult`**：使用 Pydantic 解析並驗證 LLM 回傳的 raw string，捕捉 `ValidationError` 並填入錯誤訊息。
  2. **`generate_feedback_prompt(validation_result: TaskPlanValidationResult) -> str`**：將 `validation_errors` 轉化為結構化的 Prompt 給 LLM 修正。
  3. **`generate_task_plan_with_retry(user_requirement: str, max_retries: int = 3)`**：實作 Agent 重試迴圈，成功則回傳，失敗則帶入 Feedback 繼續重試。
- **評語與測試**：經測試執行，成功發送需求並回傳符合 Schema 的完整 TaskPlan。已於 `tests/agent/test_task_plan_agent.py` 補齊 7 個單元測試案例（包含 AAA 結構驗證、Pydantic ValidationError 提取、Feedback 格式轉換與 `@patch` 模擬 LLM 的 Pass@1、Retry Feedback 修正成功與 Exceed Max Retries 測試），全專案測項達到 32/32 個 100% 通過！

---

### 【Ex-05】三層架構重構 (Service Layer, Domain Exceptions & Mock 測試)
- **完成時間**：2026-08-07
- **要求說明**：
  1. **自訂 Domain Exceptions**（`app/exceptions/exceptions.py`）：定義 `ItemNotFoundError`、`DuplicateItemError` 等業務異常。
  2. **實作 Service 層**（`app/services/ItemService.py`）：封裝業務邏輯（重複名稱檢查、查無商品拋出例外），並呼叫 `ItemRepository`。
  3. **依賴注入與重構 Router**（`app/dependencies.py` 與 `app/routers/items.py`）：透過 `Depends(get_item_service)` 注入 Service，並在 `main.py` 註冊全域 Exception Handler 將 Exception 轉為 HTTP Status Code (404, 409)。
  4. **撰寫 Service 單元測試**（`tests/services/test_item_service.py`）：使用 `unittest.mock.MagicMock` 模擬 `ItemRepository`，測試商業邏輯與例外拋出。
- **評語與測試**：經 pytest 測試，單元測試 (Unit Test) 與 API 整合測試 (Integration Test) 全部 13 個測項 100% 通過！

---

### 【Ex-06】Task REST API v0.1 & pytest 完整測試 suite (Month 1 Gate)
- **完成時間**：2026-08-08
- **要求說明**：
  1. **Task Pydantic Schemas** (`app/schemas/task.py`)：`TaskCreate`, `TaskUpdate`, `TaskResponse` (包含 status, priority)。
  2. **TaskRepository** (`app/repositories/task_repository.py`)：In-Memory Task CRUD 存取，自動生成 UUID 與 UTC 時間。
  3. **TaskService** (`app/services/task_service.py`)：封裝商業邏輯與 `TaskNotFoundError` 例外處理。
  4. **TaskRouter** (`app/routers/tasks.py`)：手寫全套 RESTful API (`POST /tasks`, `GET /tasks`, `GET /tasks/{id}`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`)。
  5. **Service 單元測試** (`tests/services/test_task_service.py`)：使用 `MagicMock` 與 AAA 結構撰寫 8 個單元測試。
  6. **API 整合測試** (`tests/tasks_api/test_tasks_api.py`)：使用 `TestClient` 與 `app.dependency_overrides` + `yield` Teardown 撰寫 5 個整合測試。
- **評語與測試**：經 pytest 測試，全專案共 25 個測項 100% 全部通過 (`25 passed in 0.75s`)！成功達成 Month 1 Gate 後端核心任務指標！

---

### 【Ex-07】Task Dependencies 有向圖 (DAG) 與循環依賴驗證
- **完成時間**：2026-08-12
- **要求說明**：
  1. **`validate_task_dependencies(task_plan: TaskPlan) -> DependencyValidationResult`**：驗證 TaskPlan 中任務之間的依賴關係。
  2. **不存在依賴 ID 檢查 (`missing_dependencies`)**：找出任務依賴了不存在於 `task_plan.tasks` 中的 Task ID。
  3. **DFS 循環依賴偵測 (`has_cycle` & `cycle_path`)**：使用深度優先搜尋 (DFS) 走訪有向圖，偵測環路並記錄完整路徑（如 `["T1", "T2", "T3", "T1"]`）。
  4. **單元測試** (`tests/agent/test_task_plan_validation.py`)：覆蓋合法 DAG、缺失依賴 ID、循環依賴路徑與自環案例。
- **評語與測試**：經 pytest 測試，全專案共 40 個測項 100% 全部通過！成功完善 Agent 的 Semantic Validation 模組。
