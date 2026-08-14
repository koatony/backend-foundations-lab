# 90天 AI System 衝刺計畫 — 練習與作業追蹤表 (EXERCISES.md)

本檔案記錄所有出過的練習題目、交付物路徑與完成狀態，方便自我進度管理與複習。

---

## 📊 專案練習進度總覽

| 編號 | 練習名稱 | 對應週次 | 主要交付物路徑 | 狀態 | 核心技術點 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ex-01** | Python 基礎與 Exception Handling | W1 | `module-import-lab/app/log_utils.py` <br> `module-import-lab/app/bank_utils.py` | ✅ 已完成 | Context Manager, Exception Bubbling, Keyword-only args |
| **Ex-02** | 手寫 JSON Validator 與 Unit Test | W1 | `module-import-lab/app/json_validator.py` <br> `module-import-lab/tests/test_json_validator.py` | ✅ 已完成 | 手寫型別/必填檢查, 自訂 Exception, pytest parameterize |
| **Ex-03** | TaskPlan Schema & Tool Parser | W2 | `fast-api-lab/app/schemas/task_plan.py` <br> `fast-api-lab/app/agent/tool_parser.py` | ✅ 已完成 | Pydantic BaseModel, Field 限制, inspect 解析函數轉 JSON Schema |
| **Ex-04** | TaskPlan Agent Loop (Generate → Validate → Feedback → Retry) | W2-W4 | `fast-api-lab/app/agent/task_plan_agent.py` <br> `fast-api-lab/tests/agent/test_task_plan_agent.py` | ✅ 已完成 | Pydantic JSON 驗證, ValidationError 提取, Feedback Prompt 產生, 重試迴圈, `@patch` Mock LLM 測試 (7/7 通過) |
| **Ex-05** | 三層架構重構 (Service Layer, Domain Exceptions & Mock 測試) | W3 | `fast-api-lab/app/services/ItemService.py` <br> `fast-api-lab/app/dependencies.py` <br> `fast-api-lab/tests/services/test_item_service.py` | ✅ 已完成 | Router-Service-Repo 三層架構解耦, 自訂 Domain Exceptions, MagicMock 隔離測試, 依賴注入 (Depends) |
| **Ex-06** | Task REST API v0.1 & pytest 完整測試 suite | W4 (Month 1 Gate) | `fast-api-lab/app/schemas/task.py` <br> `fast-api-lab/app/repositories/task_repository.py` <br> `fast-api-lab/app/services/task_service.py` <br> `fast-api-lab/app/routers/tasks.py` <br> `fast-api-lab/tests/services/test_task_service.py` <br> `fast-api-lab/tests/tasks_api/test_tasks_api.py` | ✅ 已完成 | Task CRUD 完整三層 Clean Architecture、Depends 依賴覆寫 (dependency_overrides)、Fixture 作用域、TestClient 整合測試 (25/25 通過) |
| **Ex-07** | Task Dependencies 有向圖 (DAG) 與循環依賴驗證 | W7 | `fast-api-lab/app/schemas/task_plan.py` <br> `fast-api-lab/tests/agent/test_task_plan_validation.py` | ✅ 已完成 | 有向圖 (DAG) 建立, 不存在依賴 ID 檢查, DFS 循環依賴偵測與 cycle_path 提取, pytest 單元測試 (40/40 通過) |
| **Ex-08** | PostgreSQL / SQLAlchemy ORM 與 Alembic 資料庫遷移 | W5-W6 | `fast-api-lab/app/database.py` <br> `fast-api-lab/app/models/task.py` <br> `fast-api-lab/alembic/` <br> `fast-api-lab/app/repositories/task_repository.py` <br> `fast-api-lab/tests/repositories/test_task_repositoy_db.py` | ✅ 已完成 (1.75 h) | PostgreSQL DATABASE_URL 配置, SQLAlchemy ORM Mapping (`TaskModel`), Alembic autogenerate 遷移腳本, TaskRepository 分頁/篩選, Transaction Rollback 測試, SQLite In-Memory DB 測試 |
| **Ex-09** | API 層級 DB 整合測試與 Dependency Override | W5 | `fast-api-lab/app/services/task_service.py` <br> `fast-api-lab/tests/tasks_api/test_tasks_api.py` | ✅ 已完成 (0.75 h) | FastAPI `app.dependency_overrides[get_db]`, TestClient 整合測試, API 分頁與狀態篩選測試 (51/51 通過) |

---

## 💻 C++ & 演算法 2 個月衝刺刷題追蹤表

| 模組 | 題號與名稱 | 難度 | 狀態 | 時間複雜度 | 空間複雜度 | 核心考點 / 技巧 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1. 進階雙指標與 Hash** | **LeetCode 560. Subarray Sum Equals K** | Medium | ✅ 已完成 | $O(N)$ | $O(N)$ | Prefix Sum + `unordered_map` 哈希查找 |
| **1. 進階雙指標與 Hash** | **LeetCode 15. 3Sum** | Medium | ⏳ 進行中 | $O(N^2)$ | $O(1)$ | 排序 + 雙指標 + 雙重跳過去重 |
| **1. 進階雙指標與 Hash** | **LeetCode 41. First Missing Positive** | Hard | 待完成 | $O(N)$ | $O(1)$ | In-place Hash (置換索引法) |
| **2. 單調棧與 Priority Queue** | **LeetCode 739. Daily Temperatures** | Medium | 待完成 | $O(N)$ | $O(N)$ | 單調遞減棧 (Monotonic Stack) |
| **2. 單調棧與 Priority Queue** | **LeetCode 84. Largest Rectangle in Histogram** | Hard | 待完成 | $O(N)$ | $O(N)$ | 單調遞增棧 + 哨兵節點 |
| **2. 單調棧與 Priority Queue** | **LeetCode 239. Sliding Window Maximum** | Hard | 待完成 | $O(N)$ | $O(K)$ | 單調雙端隊列 (Monotonic Deque) |
| **2. 單調棧與 Priority Queue** | **LeetCode 295. Find Median from Data Stream** | Hard | 待完成 | $O(\log N)$ | $O(N)$ | Max-Heap + Min-Heap 對頂堆設計 |

---

## 📝 練習詳細規格記錄

### 【Ex-07】Task Dependencies 有向圖 (DAG) 與循環依賴驗證
- **完成時間**：2026-08-12
- **要求說明**：
  1. **`validate_task_dependencies(task_plan: TaskPlan) -> DependencyValidationResult`**：驗證 TaskPlan 中任務之間的依賴關係。
  2. **不存在依賴 ID 檢查 (`missing_dependencies`)**：找出任務依賴了不存在於 `task_plan.tasks` 中的 Task ID。
  3. **DFS 循環依賴偵測 (`has_cycle` & `cycle_path`)**：使用深度優先搜尋 (DFS) 走訪有向圖，偵測環路並記錄完整路徑（如 `["T1", "T2", "T3", "T1"]`）。
  4. **單元測試** (`tests/agent/test_task_plan_validation.py`)：覆蓋合法 DAG、缺失依賴 ID、循環依賴路徑與自環案例。
- **評語與測試**：經 pytest 測試，全專案共 40 個測項 100% 全部通過！成功完善 Agent 的 Semantic Validation 模組。

---

### 【C++ LeetCode 560】Subarray Sum Equals K
- **完成時間**：2026-08-12
- **解題點評**：
  使用 Prefix Sum + `std::unordered_map` 的方法，在 $O(N)$ 時間與 $O(N)$ 空間內精準解出。程式碼使用 `m.find(delta)` 避免了非必要的 default insertion，`m[cur_sum]++` 放置順序正確處理了 `k = 0` 的邊界情況，表現優異！

---

### 【Ex-08】PostgreSQL / ORM 分頁篩選與 DB Transaction Rollback 測試
- **完成時間**：2026-08-14
- **要求說明**：
  1. **Pagination & Filtering**：於 `TaskRepository.list_all` 實作 `limit`、`skip` 與 `status` 條件篩選。
  2. **Router Query Parameters**：於 `GET /tasks` 透過 FastAPI `Query` 接收分頁與狀態條件。
  3. **Transaction Rollback 測試** (`test_transaction_rollback_on_error`)：在 AAA 規範下使用 `db_session.flush()` 模擬中途崩潰並執行 `db_session.rollback()`，斷言驗證資料庫無殘留廢資料。
- **點評與測試**：經 pytest 測試，`test_task_repositoy_db.py` 內 9 個 DB 測試全部正確通過！程式碼乾淨且正確遵守 Clean Architecture 解耦。

---

### 【Ex-09】API 層級 DB 整合測試與 Dependency Override
- **完成時間**：2026-08-14
- **要求說明**：
  1. **Dependency Override**：於 `tests/tasks_api/test_tasks_api.py` 中，建立 `db_session` SQLite 記憶體資料庫 fixture，並透過 `app.dependency_overrides[get_db]` 注入 API。
  2. **API 分頁與篩選測試**：實作 `test_list_tasks_with_pagination` 與 `test_list_tasks_with_status_filter`。
  3. **Service 參數對齊**：同步將 `TaskService.list_tasks` 方法加入 `skip`、`limit` 與 `status` 參數透傳。
- **點評與測試**：經 pytest 測試，專案全部 **51 個測項 100% 全部通過**！完美實現測試資料庫與正式環境的環境隔離。
