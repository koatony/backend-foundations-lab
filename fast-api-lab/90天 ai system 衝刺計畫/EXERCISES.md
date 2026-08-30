# 90天 AI System 衝刺計畫 — 實驗與細項練習題冊 (EXERCISES.md)

本檔案為專屬 **TSMC IT / 一線廠 Backend & AI Agent Systems Engineering** 的教科書式實驗手冊 (Lab Manual & Problem Set)。
- **[PLAN.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90%E5%A4%A9%20ai%20system%20%E8%A1%9D%E5%88%BA%E8%A8%88%E7%95%AB/PLAN.md)**：單元大綱、學習目標與底層導讀。
- **本檔案 (EXERCISES.md)**：一步一步帶你完成實作、驗證底層原理與進行面試問答演練的細項題目冊。

---

## 📊 專案練習細項進度總覽

| 編號 | 練習名稱 | 所屬模組 | 主要交付物路徑 | 狀態 | 🎯 核心學習與底層考點 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ex-1.1** | Exception Bubbling 與 Context Manager | Module 1 | `module-import-lab/app/log_utils.py` | 🔄 基礎完成/待底層驗證 | 資源生命週期 (`__enter__/__exit__`), 異常冒泡機制 |
| **Ex-1.2** | 手寫 Strict JSON Validator 與 pytest | Module 1 | `module-import-lab/app/json_validator.py` | 🔄 基礎完成/待底層驗證 | 手寫型別檢查, 自訂 Domain Exception, pytest 參數化 |
| **Ex-2.1** | Pydantic Field 限制與 Schema 轉化 | Module 2 | `fast-api-lab/app/schemas/task_plan.py` | 🔄 基礎完成/待底層驗證 | Pydantic BaseModel 驗證, Field 規則與型別強轉 |
| **Ex-2.2** | Python `inspect` 解析簽章轉 Schema | Module 2 | `fast-api-lab/app/agent/tool_parser.py` | 🔄 基礎完成/待底層驗證 | 語言內省 (Reflection), AST / Signature 轉化 |
| **Ex-3.1** | Generate-Validate-Retry Agent Loop | Module 3 | `fast-api-lab/app/agent/task_plan_agent.py` | 🔄 基礎完成/待底層驗證 | Structured Feedback 閉環控制, 重試收斂條件 |
| **Ex-3.2** | `@patch` Mock LLM 與 Retry 邊界測試 | Module 3 | `fast-api-lab/tests/agent/test_task_plan_agent.py` | 🔄 基礎完成/待底層驗證 | 非確定性系統測試, Mock LLM 隔離, Pass-rate 測試 |
| **Ex-4.1** | Clean Architecture 三層解耦與 Domain Exception | Module 4 | `fast-api-lab/app/services/task_service.py` | 🔄 基礎完成/待底層驗證 | Router-Service-Repo 架構解耦, 防火牆模型 |
| **Ex-4.2** | FastAPI `Depends` 與 `dependency_overrides` | Module 4 | `fast-api-lab/tests/tasks_api/test_tasks_api.py` | 🔄 基礎完成/待底層驗證 | 控制反轉 (IoC), 依賴注入生命週期, 測試連線偷天換日 |
| **Ex-5.1** | SQL 邏輯執行順序與複雜 JOIN 查詢 | Module 5 | `fast-api-lab/scripts/test_sql.sql` | ⏳ 進行中 | SQL 9 大執行順序 (`FROM` 到 `LIMIT`), 多表關聯 |
| **Ex-5.2** | Key Constraints、Cascade 與 Transaction ACID | Module 5 | `fast-api-lab/app/models/` | ⏳ 進行中 | B+Tree Unique Constraint, 外鍵級聯鎖定, ACID 特性 |
| **Ex-5.3** | 手寫 SQL 整合測試環境搭建 | Module 5 | `fast-api-lab/tests/db/test_raw_sql.py` | ⏳ 進行中 | DB Connection 手工管理, 測試資料抹除與隔離 |
| **Ex-6.1** | Unit of Work、Identity Map 與 Dirty Tracking | Module 6 | `fast-api-lab/app/repositories/task_repository.py` | 🔄 基礎完成/待底層驗證 | Session 字典快取, 自動比對生成 `UPDATE` SQL |
| **Ex-6.2** | Alembic 雙向鏈表 Revision 腳本與 Migration | Module 6 | `fast-api-lab/alembic/` | 🔄 基礎完成/待底層驗證 | DB 版本圖鏈表, `upgrade()` 與 `downgrade()` 冪等 |
| **Ex-6.3** | Transaction Savepoints 與 Rollback 隔離測試 | Module 6 | `fast-api-lab/tests/repositories/test_task_db.py` | 🔄 基礎完成/待底層驗證 | `flush()` vs `commit()`, Exception 下 WAL Undo Log 復原 |
| **Ex-7.1** | B+Tree 頁面、最左字首原則與 EXPLAIN ANALYZE | Module 7 | `fast-api-lab/scripts/explain_analysis.sql` | ⏳ 進行中 | B+Tree 樹高 3~4 層, `Seq Scan` vs `Index Only Scan` |
| **Ex-7.2** | ORM N+1 災難重現與 `selectinload` 加載模式 | Module 7 | `fast-api-lab/tests/performance/test_n_plus_one.py` | ⏳ 進行中 | Lazy Loading N+1 產生機制, `selectinload` 兩次 SQL 最優解 |
| **Ex-7.3** | DAG 有向無環圖與 DFS 三色標記法環路檢測 | Module 7 | `fast-api-lab/tests/agent/test_dag.py` | 🔄 基礎完成/待底層驗證 | DFS 三色 (White/Gray/Black), Back Edge 與拓撲排序 |
| **Ex-7.4** | PostgreSQL `pgvector` 向量檢索與 RAG 整合 | Module 7 | `fast-api-lab/app/agent/rag_retriever.py` | ⏳ 進行中 | Cosine Distance, HNSW / IVFFlat 向量索引, Tool 語意檢索 |
| **Ex-8.1** | `pydantic-settings` 環境變數動態注入解耦 | Module 8 | `fast-api-lab/app/config.py` | ⏳ 進行中 | 12-Factor App 理念, `.env` 變數自動轉型 |
| **Ex-8.2** | FastAPI 洋蔥圈 Middleware 與 Correlation ID | Module 8 | `fast-api-lab/app/middleware/logging.py` | ⏳ 進行中 | Starlette 請求/響應攔截鏈, `ContextVar` 跨協程追蹤 |
| **Ex-8.3** | Structured JSON Logging 與系統整合測試 | Module 8 | `fast-api-lab/app/utils/logger.py` | ⏳ 進行中 | ELK/Prometheus 標準 JSON 格式, Trace ID 格式化 |
| **Ex-8.4** | Token Bucket 令牌桶限流中間件實作 | Module 8 | `fast-api-lab/app/middleware/rate_limit.py` | ⏳ 進行中 | 令牌桶演算法, 防止 LLM API 額度耗盡與 HTTP 429 處理 |
| **Ex-9.1** | Linux Namespaces 與 Cgroups 硬體限額驗證 | Module 9 | `fast-api-lab/scripts/docker_test.sh` | 待完成 | PID/NET/MNT 隔離, Cgroups CPU/RAM 限制 |
| **Ex-9.2** | Multi-stage Dockerfile 與 Layer Caching | Module 9 | `fast-api-lab/Dockerfile` | 待完成 | 縮小 Image 體積, 快取層依賴優化 |
| **Ex-9.3** | Docker Compose 雙服務 Bridge 網路與 DNS 綁定 | Module 9 | `docker-compose.yml` | 待完成 | 容器間 Internal DNS 解析, 服務啟動順序依賴 |
| **Ex-10.1**| GitHub Actions CI 與 Ephemeral DB Service | Module 10 | `.github/workflows/ci.yml` | 待完成 | CI 自動化冪等測試, Service Containers 配置 |
| **Ex-10.2**| Mypy 靜態型別檢查與 Ruff Linter CI 門檻 | Module 10 | `.github/workflows/ci.yml` | 待完成 | 靜態分析抓出 `None` 引用與潛在 Bug |
| **Ex-11.1**| Cache-Aside 模式與快取穿透/擊穿/雪崩防禦 | Module 11 | `fast-api-lab/app/cache/redis_cache.py` | 待完成 | Redis 單執行緒 Reactor, Bloom Filter / Random Jitter |
| **Ex-11.2**| Circuit Breaker 熔斷器模式三態狀態機實作 | Module 11 | `fast-api-lab/app/utils/circuit_breaker.py`| 待完成 | Closed/Open/Half-Open 狀態機, 防止下游相依服務雪崩 |
| **Ex-11.3**| SQLAlchemy `QueuePool` 調優與連線池防禦 | Module 11 | `fast-api-lab/app/database.py` | 待完成 | TCP 三次握手複用, `pool_size` 與 overflow 配置 |
| **Ex-12.1**| Agent Benchmark Evaluator 評估系統 | Module 12 | `fast-api-lab/app/agent/evaluator.py` | 待完成 | Schema Pass Rate, Avg Token Cost, Latency 統計 |
| **Ex-12.2**| 無 AI 限時白板 API 與一線大廠系統架構問答 | Module 12 | `docs/mock_interview_notes.md` | 待完成 | 白板手寫程式碼、系統設計與技術面試攻防 |

---

## 📝 題目詳細規格說明書 (教科書式練習題)

### 【Module 1: Python 高級語言特性與例外架構】

#### 📌 【Ex-1.1】Exception Bubbling 與 Context Manager 實作
- **實作任務**：在 `app/log_utils.py` 實作自訂 Context Manager `timer()`，記錄區塊執行時間；並在 `app/bank_utils.py` 模擬階層式 Exception Bubbling。
- **🎯 這題要弄懂的底層原理**：
  1. Python `with` 語句觸發 `__enter__()` 與 `__exit__(exc_type, exc_val, exc_tb)` 的生命週期。
  2. 當 `__exit__` 回傳 `True` 時會吞掉 Exception，回傳 `False` 時異常會持續往上層 Call Stack 冒泡 (Bubbling)。
- **🧪 驗證與交付條件**：寫 pytest 驗證 `timer()` 正常輸出日誌，且特意拋出 Exception 時，Context Manager 能正確關閉資源並將 Exception 傳給外層。
- **💡 大廠面試深挖必考題**：
  > *「如果在 `__enter__` 成功後、執行內文時突然發生系統崩潰，`__exit__` 保證會被執行嗎？`finally` 與 Context Manager 有何異同？」*

---

#### 📌 【Ex-1.2】手寫 Strict JSON Validator 與 pytest 矩陣測試
- **實作任務**：不使用 Pydantic，手寫 `validate_json(data: dict, schema: dict)`，若欄位缺失或型別不符合則拋出 `InvalidPayloadError`。
- **🎯 這題要弄懂的底層原理**：
  1. 動態型別語言 (Python) 缺乏編譯期檢查，如何在 Runtime 建立嚴格的 Domain Exception 防火牆。
  2. pytest `@pytest.mark.parametrize` 測試矩陣的運行機制（每次傳參建立獨立測試個案，隔離全域狀態）。
- **🧪 驗證與交付條件**：`tests/test_json_validator.py` 包含至少 8 個測試案例（含型別錯誤、必填缺失、多餘欄位、嵌套字典）。
- **💡 大廠面試深挖必考題**：
  > *「為什麼正式專案不鼓勵直接使用 Python 內建的 `assert` 來做業務邏輯檢查？」*（提示：`python -O` 優化模式會直接忽略 assert）。

---

### 【Module 2: Pydantic Schema 限制與 LLM Tool Parsing】

#### 📌 【Ex-2.1】Pydantic Field 限制與 Schema 轉化
- **實作任務**：在 `app/schemas/task_plan.py` 定義 `TaskPlan` 與 `TaskItem`，加入 `Field(min_length=1, max_length=100)` 與正規表示式 Regex 限制。
- **🎯 這題要弄懂的底層原理**：
  1. Pydantic 的資料解析 (Parsing) vs 驗證 (Validation)：如何將外部不可信的非結構化 JSON 強轉型並清洗。
  2. `BaseModel.model_json_schema()` 產生標準 JSON Schema 的機制，作為 LLM Function Calling 的約束規範。
- **🧪 驗證與交付條件**：單元測試驗證傳入非法字元或超過長度限制時拋出 `pydantic.ValidationError`。
- **💡 大廠面試深挖必考題**：
  > *「Pydantic V1 與 V2 在底層效能上有何重大變革？」*（提示：Pydantic-core 由 Rust 重寫，加速 5~20 倍）。

---

#### 📌 【Ex-2.2】Python `inspect` 解析簽章轉 Schema
- **實作任務**：在 `app/agent/tool_parser.py` 實作 `function_to_json_schema(func)`，自動利用 `inspect.signature` 解析 Python 函數 Docstring 與 Type Hints。
- **🎯 這題要弄懂的底層原理**：
  1. Python 語言的**內省 (Introspection)** 機制：如何在 Runtime 動態讀取函數簽章、參數預設值與型別標註。
  2. 將原生 Python 函數簽章轉換為 OpenAI / Gemini Tool Definition 格式。
- **🧪 驗證與交付條件**：測試傳入任意帶 Type Hints 的函數，能自動輸出合法的 OpenAPI 格式 Tool Schema。
- **💡 大廠面試深挖必考題**：
  > *「`inspect.getmembers()` 與 `getattr()` 在動態框架底層如何運作？有何安全性風險？」*

---

### 【Module 3: 不依賴框架的 Agent Loop 與 Structured Feedback】

#### 📌 【Ex-3.1】Generate-Validate-Retry Agent Loop
- **實作任務**：在 `app/agent/task_plan_agent.py` 實作不依賴 LangChain 的自研 Agent Loop（LLM 產生 ➡️ Pydantic 驗證 ➡️ 抓出 ValidationError ➡️ 組合 Feedback Prompt ➡️ 重試）。
- **🎯 這題要弄懂的底層原理**：
  1. **閉環控制理論 (Feedback Control Loop)**：如何將非確定性的 LLM 輸出轉化為具備 100% 確定性 (Deterministic) 的後端資料結構。
  2. **收斂策略**：設定最大重試次數 `max_retries=3`，防止無效遞迴引發 Token 耗盡。
- **🧪 驗證與交付條件**：驗證當 LLM 第一次回傳格式錯誤 JSON 時，能自動將錯誤詳情反饋給 LLM 並在第二次重試成功產出合法物件。
- **💡 大廠面試深挖必考題**：
  > *「在企業級 Agent 架構中，為什麼自研輕量 Controller 比直接使用 LangChain 更加可控且易於除錯？」*

---

#### 📌 【Ex-3.2】`@patch` Mock LLM 與 Retry 邊界測試
- **實作任務**：在 `tests/agent/test_task_plan_agent.py` 中使用 `unittest.mock.patch` 模擬 LLM API 的各種極端回應（格式錯誤、部分缺失、網路超時）。
- **🎯 這題要弄懂的底層原理**：
  1. **單元測試的隔離性 (Isolation)**：測試 Agent 邏輯時不應實際連網消耗 Token，且需消除網路延遲波動。
  2. Mock 物件的 `side_effect` 模擬連續不同回應（第 1 次失敗 ➡️ 第 2 次成功）。
- **🧪 驗證與交付條件**：7 個測試案例 100% 通過，涵蓋一次成功、二次成功、超過最大重試次數拋出 `AgentRetryLimitExceededError`。
- **💡 大廠面試深挖必考題**：
  > *「如何測試一個本質上具備隨機性 (Temperature > 0) 的 AI Agent 系統？」*

---

### 【Module 4: Clean Architecture 三層解耦與依賴注入】

#### 📌 【Ex-4.1】Clean Architecture 三層解耦與 Domain Exception
- **實作任務**：重構 Task 模組，劃分為 Router 層 (HTTP 介面) ➡️ Service 層 (商業邏輯) ➡️ Repository 層 (資料存取)，並定義自訂 `TaskNotFoundError`。
- **🎯 這題要弄懂的底層原理**：
  1. **關注點分離 (Separation of Concerns)**：Router 不直接操作資料庫，Repository 不感知 HTTP 狀態碼。
  2. **DTO (Data Transfer Object) 防火牆**：`TaskModel` (DB 實體) 與 `TaskResponse` (前端 Schema) 徹底解耦。
- **🧪 驗證與交付條件**：使用 `MagicMock` 模擬 Repository，在不連接資料庫的情況下對 `TaskService` 進行 100% 覆蓋的單元測試。
- **💡 大廠面試深挖必考題**：
  > *「為什麼在現代後端系統中，不能直接把 ORM Model 作為 API Response 回傳給前端？」*

---

#### 📌 【Ex-4.2】FastAPI `Depends` 與 `dependency_overrides`
- **實作任務**：在 `app/dependencies.py` 定義 `get_task_service` 與 `get_db`；在測試中使用 `app.dependency_overrides` 注入 Mock 物件。
- **🎯 這題要弄懂的底層原理**：
  1. **控制反轉 (Inversion of Control, IoC)**：物件的生命週期與依賴關係由 FastAPI 框架容器管理。
  2. **測試隔離技術**：在不改動任何生產環境程式碼的前提下，在測試執行期間動態置換底層連線。
- **🧪 驗證與交付條件**：API 整合測試中，FastAPI Router 正確接收到被覆寫的 Mock Service，並回傳預期的 Mock 資料。
- **💡 大廠面試深挖必考題**：
  > *「FastAPI 的 `Depends` 是在什麼時機點被執行的？它是 Singleton (單例) 還是 Request-Scoped (每個請求獨立)？」*

---

### 【Module 5: SQL 語法執行順序與 PostgreSQL 機制】

#### 📌 【Ex-5.1】SQL 邏輯執行順序與複雜 JOIN 查詢
- **實作任務**：撰寫手寫 SQL 腳本 `scripts/test_sql.sql`，找出「在過去 30 天內發布超過 5 個 Task 且平均完成時間最短的前 3 名 User」。
- **🎯 這題要弄懂的底層原理**：
  1. SQL 的**邏輯執行順序**：`FROM` ➡️ `ON` ➡️ `JOIN` ➡️ `WHERE` ➡️ `GROUP BY` ➡️ `HAVING` ➡️ `SELECT` ➡️ `ORDER BY` ➡️ `LIMIT`。
  2. 為什麼在 `WHERE` 條件句中不能使用 `SELECT` 宣告的聚合別名（如 `WHERE total_count > 5` 會報錯）？因為 `WHERE` 的執行階段早於 `SELECT`！
- **🧪 驗證與交付條件**：SQL 語法正確使用 `HAVING count(t.id) > 5` 進行聚合後篩選，並在 psql 命令列執行順利產出正確結果。
- **💡 大廠面試深挖必考題**：
  > *「`WHERE` 篩選與 `HAVING` 篩選在底層執行效能上有何本質區別？為什麼能用 `WHERE` 就不要放在 `HAVING` 處理？」*

---

#### 📌 【Ex-5.2】Key Constraints、Cascade 與 Transaction ACID
- **實作任務**：在 PostgreSQL 中定義 `users` 與 `tasks` 表，設置 `FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE`。
- **🎯 這題要弄懂的底層原理**：
  1. **B+Tree Unique Constraint**：主鍵 (PK) 索引如何利用 B+Tree 葉子節點的唯一性快速檢測重複插入。
  2. **ACID 中的 Durability (持久性)**：PostgreSQL 如何透過 **WAL (Write-Ahead Logging)** 預寫日誌，在硬體突發斷電時利用 WAL 進行 Crash Recovery。
- **🧪 驗證與交付條件**：當刪除 `users` 表的某一列時，Postgres 自動觸發級聯刪除該用戶對應的所有 `tasks` 列；並驗證包含非法 Foreign Key 的 Insert 操作會被 DB 強制駁回。
- **💡 大廠面試深挖必考題**：
  > *「什麼是資料庫的 WAL (Write-Ahead Log)？為什麼先寫日誌到 Disk 比直接寫資料頁 (Data Page) 快得多？」*（提示：隨機 I/O vs 順序 I/O）。

---

#### 📌 【Ex-5.3】手寫 SQL 整合測試環境搭建
- **實作任務**：在 `tests/db/test_raw_sql.py` 中撰寫原生 DB 連線整合測試，手動管理 Connection 的開閉與 Transaction 提交。
- **🎯 這題要弄懂的底層原理**：
  1. 原生 DB Driver (如 `psycopg2` / `asyncpg`) 的連線生命週期與 Socket 通訊。
  2. 手動處理 `cursor.execute()` 與測試後的資料庫清理 (Tear-down Database Cleanup)。
- **🧪 驗證與交付條件**：pytest 能正確連接實體 PostgreSQL 執行建表、插入、查詢並在測試結束後清空測試資料庫。
- **💡 大廠面試深挖必考題**：
  > *「資料庫游標 (Cursor) 在底層記憶體中是如何運作的？為什麼處理百萬筆大數據時必須使用 Server-side Cursor？」*

---

### 【Module 6: SQLAlchemy ORM 運轉機制與 Alembic 遷移】

#### 📌 【Ex-6.1】Unit of Work、Identity Map 與 Dirty Tracking 驗證
- **實作任務**：在 `TaskRepository` 內存取一個 `TaskModel`，修改其 `status` 屬性，不呼叫任何 update 方法，直接呼叫 `db.commit()`。
- **🎯 這題要弄懂的底層原理**：
  1. **Identity Map 模式**：SQLAlchemy Session 內置字典，確保同一個 Transaction 內相同 PK 的列只會有一個 Python 物件實例。
  2. **Dirty Tracking 機制**：Session 在 `flush()` 時比對物件的原始狀態快照 (Snapshot) 與當前屬性，自動生成精準的 `UPDATE tasks SET status = ... WHERE id = ...` SQL。
- **🧪 驗證與交付條件**：撰寫測試證明修改屬性後 `db.commit()` 能成功寫入 DB，並印出 SQLAlchemy 實際發出的 `UPDATE` SQL 語法。
- **💡 大廠面試深挖必考題**：
  > *「SQLAlchemy Session 的 `flush()` 與 `commit()` 有何區別？呼叫 `flush()` 時 SQL 發送了嗎？資料庫 Transaction 結束了嗎？」*

---

#### 📌 【Ex-6.2】Alembic 雙向鏈表 Revision 腳本與 Migration
- **實作任務**：初始化 Alembic 環境，為 `TaskModel` 生成自動遷移腳本 (`alembic revision --autogenerate`)，並測試 `upgrade head` 與 `downgrade -1`。
- **🎯 這題要弄懂的底層原理**：
  1. **版本圖 (Revision Chain)**：Alembic 如何利用雙向鏈表 (`revision` 與 `down_revision`) 追蹤資料庫 Schema 的歷史演進。
  2. **Schema 差異比對 (Diffing)**：比對 Python `Base.metadata` 與資料庫 `information_schema` 的欄位差異。
- **🧪 驗證與交付條件**：成功在 SQLite 與 PostgreSQL 兩種資料庫上執行遷移腳本，且降級後 Schema 完美復原無報錯。
- **💡 大廠面試深挖必考題**：
  > *「在多人協同開發時，如果兩個人同時生成了新的 Alembic Migration 導致 Branch Merge 衝突（多個 head），應該如何解決？」*

---

#### 📌 【Ex-6.3】Transaction Savepoints 與 Rollback 隔離測試
- **實作任務**：撰寫 `test_transaction_rollback_on_error` 與 `test_transaction_savepoint_partial_rollback`，驗證全盤回滾 (Full Rollback) 與利用 SQLAlchemy `session.begin_nested()` (SAVEPOINT) 進行局部回滾 (Partial Rollback)。
- **🎯 這題要弄懂的底層原理**：
  1. **Atomicity (原子性)**：Transaction 內的操作「要麼全部成功，要麼全部失敗」。
  2. **Savepoint (保存點 `SAVEPOINT`)** 與 **Rollback**：當批次處理資料時，可利用保存點做區域性隔離撤銷，防止單一無效資料導致整個大型交易做白工。當 DB 丟出 Exception 時，該 Session 連線會進入 `Aborted` 狀態，必須顯式呼叫 `rollback()` 才能釋放連線回 Pooling。
- **🧪 驗證與交付條件**：pytest 斷言全盤回滾筆數為 0；並斷言 Savepoint 局部回滾能成功保留前幾筆有效資料，第 3 筆異常被單獨撤銷，且 DB Session 仍能正常執行下一筆查詢（無 `InFailedSqlTransaction` 錯誤）。
- **💡 大廠面試深挖必考題**：
  > *「巨量資料批次處理中，若某筆資料格式錯誤不希望全盤撤銷，如何在 ORM 與 SQL 層使用 Savepoint (`begin_nested()`) 做局部隔離回滾？」*

---

### 【Module 7: 資料庫調優、pgvector 向量檢索與圖論 DAG 驗證】

#### ✅ 【Ex-7.1】B+Tree 頁面、最左字首原則與 EXPLAIN ANALYZE 診斷 (已完成)
- **實作任務**：在 Postgres 中插入 100,000 筆 Task 資料，建立複合索引 `CREATE INDEX idx_status_created ON tasks(status, created_at)`，並執行 `EXPLAIN ANALYZE` 觀察查詢計畫。
- **🎯 這題要弄懂的底層原理**：
  1. **B+Tree 頁面結構與 Fan-out**：B+Tree 樹高僅 3~4 層，磁碟 I/O 次數極少。
  2. **最左字首原則 (Leftmost Prefix Rule)**：複合索引 `(status, created_at)` 索引樹是先按 `status` 排序，再按 `created_at` 排序。只查 `WHERE created_at = ?` 無法使用該索引！
  3. **Scan 類型**：`Seq Scan` (全表) vs `Index Scan` (回表 Heap Fetch) vs `Index Only Scan` (Covering Index 免回表)。
- **🧪 驗證與交付條件**：比較 `WHERE status = 'PENDING' AND created_at > ...` (`Index Scan`) 與 `WHERE created_at > ...` (`Seq Scan`) 的 Cost 與 Execution Time 差異，並寫成分析報告。
- **💡 大廠面試深挖必考題（參見 [TSMC面試必考.md - 題 1.1 / 題 1.2](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/TSMC面試必考.md#-主題一資料庫與物理-io-調優-database--disk-io)）**：
  > 1. *「什麼是 Covering Index（覆蓋索引）？`SELECT id, age` 能走 `Index Only Scan`，但加了 `SELECT name` 為什麼會退化成回表？如何消除隨機 Read？」*
  > 2. *「深度分頁 `LIMIT 10 OFFSET 1000000` 為何引發百萬次無用物理回表？如何使用 Deferred Join 重構？」*


---

#### 📌 【Ex-7.2】ORM N+1 災難重現與 `selectinload` 加載模式對比
- **實作任務**：在 `test_n_plus_one.py` 中故意寫出 N+1 迴圈查詢（撈 50 個 User 並印出各自的 Tasks）；接著使用 `selectinload(User.tasks)` 重構。
- **🎯 這題要弄懂的底層原理**：
  1. **N+1 災難成因**：Lazy Loading 導致 1 次主查詢 + N 次關聯子查詢，產生 51 次 SQL RTT (Round Trip Time)。
  2. **三種 SQL 加載模式權衡**：
     - `joinedload`：使用 `LEFT OUTER JOIN`（1 次 SQL，但有多對多笛卡兒積資料重複爆量風險）。
     - `selectinload`：發送 2 次 SQL（`WHERE user_id IN (1, 2, ..., 50)`，效能最好且無笛卡兒積，一對多最推薦）。
- **🧪 驗證與交付條件**：使用 SQLAlchemy 的 Query Count Listener 斷言重構前 SQL 發送次數為 51 次，重構後精準降為 2 次！
- **💡 大廠面試深挖必考題**：
  > *「為什麼在分頁 (Pagination `LIMIT/OFFSET`) 的情況下，使用 `joinedload` 往往會產生錯誤的 Limit 結果？應該如何解決？」*

---

#### 📌 【Ex-7.3】DAG 有向無環圖與 DFS 三色標記法環路檢測
- **實作任務**：在 `app/agent/task_plan_agent.py` 中實作 `detect_cycle_dfs(tasks)`，傳回是否包含循環依賴及完整環路路徑 `["T1", "T2", "T1"]`。
- **🎯 這題要弄懂的底層原理**：
  1. **DFS 三色標記法 (White/Gray/Black)**：
     - **White (0)**：未造訪。
     - **Gray (1)**：當前 recursion stack 正在探索中。遇到 Gray 節點即代表發現 **Back Edge (後退邊)**，證明有環！
     - **Black (2)**：該節點及其子樹已完全探索完畢。
- **🧪 驗證與交付條件**：pytest 覆蓋自環 (`T1->T1`)、簡單環 (`T1->T2->T1`)、長環路 (`T1->T2->T3->T4->T2`) 及合法 DAG 案例（40/40 測試通過）。
- **💡 大廠面試深挖必考題**：
  > *「除了 DFS 三色標記法，拓撲排序 (Topological Sort) 的 Kahn 演算法 (Kahn's Algorithm - 入度佇列) 是如何檢測圖中有環的？」*

---

#### 📌 【Ex-7.4】PostgreSQL `pgvector` 向量檢索與 RAG 整合
- **實作任務**：在 `app/agent/rag_retriever.py` 整合 `pgvector`，將 Tool 規格與任務歷史存入 Embedding 向量欄位，實作 Top-K 語意相似度檢索。
- **🎯 這題要弄懂的底層原理**：
  1. **向量距離計算**：Cosine Distance vs L2 Euclidean Distance。
  2. **向量索引 (Vector Index)**：**IVFFlat** (倒排聚類) vs **HNSW** (Hierarchical Navigable Small World, 階層式導航小世界圖) 之查詢延遲與記憶體權衡。
- **🧪 驗證與交付條件**：透過 SQL `<=>` 操作符檢索最相符的 3 個 Tool 簽章，並驗證檢索耗時在 10ms 以內。
- **💡 大廠面試深挖必考題**：
  > *「為什麼在生產環境的 RAG 系統中，單純的向量檢索 (Dense Retrieval) 往往不如加上 BM25 關鍵字檢索的混合檢索 (Hybrid Search)？」*

---

### 【Module 8: 系統基建、Correlation ID 與限流保護】

#### 📌 【Ex-8.1】`pydantic-settings` 環境變數動態注入解耦
- **實作任務**：在 `app/config.py` 定義 `Settings(BaseSettings)`，支援從 `.env` 檔案載入 `DATABASE_URL`、`API_KEY` 與 `ENVIRONMENT`。
- **🎯 這題要弄懂的底層原理**：
  1. **12-Factor App 第三條 (Config)**：程式碼 (Code) 與設定檔 (Config) 徹底解耦，禁止將連線密碼寫死於 Git 倉庫。
  2. 型別自動轉型 (Type Coercion) 與預設值 Fallback 處理。
- **🧪 驗證與交付條件**：當切換環境變數 `ENV=production` 時，應用程式能自動載入對應環境之 DB 連線字串。
- **💡 大廠面試深挖必考題**：
  > *「在 Kubernetes / Docker 生態系中，環境變數是如何從 ConfigMap / Secret 注入到容器內部的？」*

---

#### 📌 【Ex-8.2】FastAPI 洋蔥圈 Middleware 與 Correlation ID
- **實作任務**：在 `app/middleware/logging.py` 實作 Middleware，攔截所有進出請求，自動生成 `X-Request-ID` (UUID) 寫入 Response Header，並存入 Python `ContextVar`。
- **🎯 這題要弄懂的底層原理**：
  1. **Starlette ASGI Middleware 洋蔥圈模型**：請求進入與回應離開皆經過攔截器鏈 (Interceptor Chain)。
  2. **Python `ContextVar` 機制**：在非同步協程 (Coroutine) 併發環境中，確保每個非同步 Request 擁有獨立的上下文變數，不發生全域變數競爭 (Race Condition)。
- **🧪 驗證與交付條件**：發送 HTTP 請求，驗證 Response Header 包含 `X-Request-ID`，且後端 Log 每行皆印出相同的 Request ID。
- **💡 大廠面試深挖必考題**：
  > *「為什麼在 Python Asyncio 非同步程式中，不能用 `threading.local()` 來儲存 Request ID？」*

---

#### 📌 【Ex-8.3】Structured JSON Logging 與系統整合測試
- **實作任務**：在 `app/utils/logger.py` 配置標準 Structured JSON 日誌輸出器，包含 `timestamp`, `level`, `request_id`, `message`, `duration_ms`。
- **🎯 這題要弄懂的底層原理**：
  1. **可觀測性 (Observability)**：結構化日誌（JSON 格式）讓 ELK (Elasticsearch/Logstash/Kibana) 或 Grafana Loki 能進行毫秒級快速解析與索引。
- **🧪 驗證與交付條件**：執行 API 整合測試，驗證輸出的每一行 log 均符合標準 JSON 格式且能被 `json.loads()` 正確解析。
- **💡 大廠面試深挖必考題**：
  > *「純文字 Log (Plaintext Log) 與結構化 JSON Log 在大型微服務分散式系統日誌收集中有何關鍵差異？」*

---

#### 📌 【Ex-8.4】Token Bucket 令牌桶限流中間件實作
- **實作任務**：在 `app/middleware/rate_limit.py` 實作 Token Bucket 限流演算法，對每秒超過限制的請求回傳 `429 Too Many Requests` 與 `Retry-After` Header。
- **🎯 這題要弄懂的底層原理**：
  1. **Token Bucket (令牌桶) 演算法原理**：固定速率向桶子放入 Token，請求消耗 Token，支援突發流量 (Burst)。
  2. **保護下游 LLM API 額度**：防止惡意或高併發 Request 刷爆 LLM Provider 的 Rate Limit。
- **🧪 驗證與交付條件**：發送 50 個併發請求，前 20 個成功通過 (200 OK)，後續請求精準收到 429 狀態碼。
- **💡 大廠面試深挖必考題**：
  > *「Token Bucket (令牌桶) 與 Leaky Bucket (漏桶) 在應對突發流量 (Traffic Burst) 時的行為有何不同？」*

---

### 【Module 9: Linux 容器化、Multi-stage Dockerfile 與 Docker Compose】

#### 📌 【Ex-9.1】Linux Namespaces 與 Cgroups 硬體限額驗證
- **實作任務**：撰寫 `scripts/docker_test.sh`，在 Linux 上啟動 Docker 容器，設定 `--cpus="1.0" --memory="512m"` 資源上限並驗證進程隔離。
- **🎯 這題要弄懂的底層原理**：
  1. **Linux Namespaces**：PID (進程隔離)、NET (網路隔離)、MNT (掛載點隔離)、IPC (行程間通訊隔離)。
  2. **Linux Cgroups (Control Groups)**：限制進程樹的 CPU 核心配額與記憶體上限，防止單一服務 OOM 拖垮整個宿主機。
- **🧪 驗證與交付條件**：進入容器內部執行 `ps aux` 驗證 PID 1 隔離，並透過 `docker stats` 驗證記憶體超載時被 Cgroups 限制。
- **💡 大廠面試深挖必考題**：
  > *「容器 (Container) 與虛擬機 (Virtual Machine, VM) 在作業系統核心 (Kernel) 與硬體抽象層有何本質區別？」*

---

#### 📌 【Ex-9.2】Multi-stage Dockerfile 與 Layer Caching
- **實作任務**：為 FastAPI 專案撰寫 `Dockerfile`，採用多階段構建 (Builder Stage ➡️ Runner Stage)，先 `COPY requirements.txt` 再 `COPY . .`。
- **🎯 這題要弄懂的底層原理**：
  1. **Docker Layer Caching**：Docker 構建時以指令為單位產生唯讀層。依賴檔案未變更時重用 Cache，秒級完成 Build。
  2. **Multi-stage Build**：編譯依賴 (GCC、標頭檔、快取) 留在 Builder Stage，最終映像檔僅包含極簡 Runtime，體積縮小 80%。
- **🧪 驗證與交付條件**：構建出的 Image 體積小於 200MB，且修改原始碼後二次 build 時間小於 3 秒。
- **💡 大廠面試深挖必考題**：
  > *「為什麼在正式生產環境 Docker 鏡像中，嚴禁使用 `root` 使用者來執行 Web 應用程式？」*

---

#### 📌 【Ex-9.3】Docker Compose 雙服務 Bridge 網路與 DNS 綁定
- **實作任務**：撰寫 `docker-compose.yml`，定義 `web` (FastAPI) 與 `db` (PostgreSQL) 服務，配置 `healthcheck` 與 `depends_on: condition: service_healthy`。
- **🎯 這題要弄懂的底層原理**：
  1. **Docker Internal DNS**：Docker Compose 自建 Bridge 網路，容器直接透過 Service Name (如 `http://db:5432`) 進行內部通信。
  2. **服務啟動依賴陷阱**：`depends_on` 預設只等待容器啟動 (Started)，而非資料庫就緒 (Ready)；必須搭配 Healthcheck 防止 Web 啟動時 DB 尚未就緒報錯。
- **🧪 驗證與交付條件**：執行 `docker compose up -d` 能一鍵拉起整套系統，且 Web 容器等待 DB 健康檢查通過後才開始連線。
- **💡 大廠面試深挖必考題**：
  > *「在 Docker Compose 中，Host 模式網路與 Bridge 模式網路有何差異與適用場景？」*

---

### 【Module 10: CI/CD Pipeline 自動化與 Service Containers】

#### 📌 【Ex-10.1】GitHub Actions CI 與 Ephemeral DB Service
- **實作任務**：在 `.github/workflows/ci.yml` 設定 CI 流程，在 `git push` 時拉起 PostgreSQL Service Container 並自動執行 `pytest`。
- **🎯 這題要弄懂的底層原理**：
  1. **CI Pipeline 冪等性 (Idempotency)**：每次 CI 執行都是建立在乾淨且可拋棄的短暫容器 (Ephemeral Container) 中，杜絕環境污染。
  2. **Service Containers**：在 GitHub Actions Runner 內部建立容器網路，供測試步驟連線。
- **🧪 驗證與交付條件**：提交 Pull Request 觸發 GitHub Actions，自動執行所有單元測試與資料庫整合測試並回傳綠燈。
- **💡 大廠面試深挖必考題**：
  > *「在 CI/CD 流程中，如何有效快取 pip 或 npm 依賴以減少 70% 的建置時間？」*

---

#### 📌 【Ex-10.2】Mypy 靜態型別檢查與 Ruff Linter CI 門檻
- **實作任務**：在 CI 流程中加入 `ruff check .` 與 `mypy --strict app/` 檢查步驟。
- **🎯 這題要弄懂的底層原理**：
  1. **靜態分析 (Static Code Analysis)**：在不執行程式碼的情況下，透過 AST 語法樹檢查出未引用的變數、`Optional[T]` 未判斷 `None` 導致的 `AttributeError`。
- **🧪 驗證與交付條件**：故意在 Code 中引入型別不匹配錯誤，CI 流程精準攔截並報錯中斷。
- **💡 大廠面試深挖必考題**：
  > *「Python 的 Type Hint 在 Runtime 會有額外的效能開銷嗎？它與 Java / C++ 的靜態型別有何異同？」*

---

### 【Module 11: 高併發系統設計 — 快取策略、熔斷器與連線池調優】

#### 📌 【Ex-11.1】Cache-Aside 模式與快取三大災難防禦
- **實作任務**：在 `app/cache/redis_cache.py` 實作 API 快取層，採用 **Cache-Aside Pattern**，並加入快取穿透與雪崩防禦。
- **🎯 這題要弄懂的底層原理**：
  1. **Cache-Aside 流程**：先讀 Cache ➡️ 命中則回傳 ➡️ 未命中則讀 DB ➡️ 寫入 Cache ➡️ 回傳。
  2. **快取三大災難與防禦**：
     - **快取穿透 (Penetration)**：查詢不存在的 Key 導致直接刷爆 DB。防禦：快取空值 (`None`) 或使用布隆過濾器 (Bloom Filter)。
     - **快取擊穿 (Breakdown)**：熱點 Key 到期的瞬間高併發衝擊 DB。防禦：互斥鎖 (Distributed Lock) 重新載入。
     - **快取雪崩 (Avalanche)**：大量 Key 在同一時間集中到期。防禦：TTL 加上隨機抖動值 (Random Jitter, 如 $300 \pm 30$ 秒)。
- **🧪 驗證與交付條件**：測試當 DB 查無資料時，快取層能寫入短暫空值，防止連續請求直擊 DB；並證明 TTL 帶有 Jitter 隨機值。
- **💡 大廠面試深挖必考題**：
  > *「當更新資料庫時，應該是『先更新 DB 再刪除 Cache』還是『先刪除 Cache 再更新 DB』？為什麼後者在併發下會導致舊資料髒讀？」*

---

#### 📌 【Ex-11.2】Circuit Breaker 熔斷器模式三態狀態機實作
- **實作任務**：在 `app/utils/circuit_breaker.py` 實作熔斷器類別，包裹對外部 LLM API 的呼叫。
- **🎯 這題要弄懂的底層原理**：
  1. **熔斷器三態狀態機 (Closed ➡️ Open ➡️ Half-Open)**：
     - **Closed**：正常狀態，失敗率達閾值時轉移至 Open。
     - **Open**：直接拒絕呼叫，觸發 Fallback 降級，保護下游不被壓垮。
     - **Half-Open**：冷卻時間過後，允許少量請求試探，若成功則恢復 Closed。
- **🧪 驗證與交付條件**：模擬外部 API 連續拋出 5 次 500 錯誤，熔斷器立即轉為 Open 並在 0ms 內回傳 Fallback 預設值。
- **💡 大廠面試深挖必考題**：
  > *「在分散式微服務架構中，為什麼 Circuit Breaker (熔斷器) 通常要與 Exponential Backoff (指數退避重試) 搭配使用？」*

---

#### 📌 【Ex-11.3】SQLAlchemy `QueuePool` 調優與連線池防禦
- **實作任務**：在 `app/database.py` 配置 SQLAlchemy `create_engine` 參數：`pool_size=5`, `max_overflow=10`, `pool_timeout=30`, `pool_recycle=1800`。
- **🎯 這題要弄懂的底層原理**：
  1. **TCP 開銷與連線池複用**：建立 Postgres TCP 連線包含三次握手、TLS 與身份驗證，耗時 50~100ms。Pooling 將長連線保持在記憶體中複用。
  2. **Pool Overflow 與 Timeout**：當併發請求超過 `pool_size + max_overflow` 時，新請求會在 `pool_timeout` 時間內等待；超時則拋出 `TimeoutError` 防止 Server 記憶體被撐爆。
- **🧪 驗證與交付條件**：模擬 20 個併發 Task 同時索取 DB 連線，驗證連線池成功控管在 15 條連線以內，且超過限制時正確拋出 Timeout 異常。
- **💡 大廠面試深挖必考題**：
  > *「為什麼 Postgres 後端資料庫設定 `max_connections=100`，而我們應用程式連線池 `pool_size` 通常設 10~20 反而比設 100 效能更高？」*（提示：CPU Context Switch 與 Disk I/O 競爭）。

---

### 【Module 12: Agent Benchmark 評估系統與白板技術面試】

#### 📌 【Ex-12.1】Agent Benchmark Evaluator 評估系統
- **實作任務**：在 `app/agent/evaluator.py` 實作自動化 Benchmark 評估腳本，執行 30 個測試情境並產出 `reports/agent_evaluation.md`。
- **🎯 這題要弄懂的底層原理**：
  1. **Agent 關鍵評估指標**：Schema Pass Rate (格式正確率)、First-attempt Pass Rate (一次通過率)、Average Latency、Average Token Cost。
  2. **邊界案例 (Edge Cases)**：測試超長 Context、格式損壞 JSON、惡意 Prompt Injection 對系統魯棒性的影響。
- **🧪 驗證與交付條件**：自動生成包含各指標表格與失敗案例深入分析的 Markdown 評估報告。
- **💡 大廠面試深挖必考題**：
  > *「如何評估一個生產環境中的 AI Agent 是否具備足夠的穩定性 (Reliability) 可以上線交付？」*

---

#### 📌 【Ex-12.2】無 AI 限時白板 API 與一線大廠系統架構問答
- **實作任務**：在 45 分鐘內，不借助任何 AI 輔助，純手寫一個具備 Pydantic 驗證、SQLAlchemy ORM 查詢、Exception 處理與單元測試的小型 REST API；並進行模擬技術面試攻防。
- **🎯 這題要弄懂的底層原理**：
  1. **技術肌肉記憶與自主架構力**：證明自己不是依賴 AI 的複製貼上者，而是能在面試白板與真實生產環境中快速除錯、決策架構的資深工程師。
- **🧪 驗證與交付條件**：完成 `docs/mock_interview_notes.md`，整理 20 道高頻後端/AI 系統面試問答與自身專案架構亮點。
- **💡 大廠面試深挖必考題**：
  > *「請在白板上畫出你這個 AI TaskPlan 系統的完整架構圖，並說明當每秒請求量 (QPS) 從 10 暴增到 10,000 時，你會如何在資料庫、快取與 Agent 層面進行架構擴展 (Scaling)？」*
