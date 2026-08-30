# 90天 AI System 衝刺計畫 — Backend & Agent 核心學習筆記 (BACKEND_AGENT_NOTES.md)

本筆記本用於紀錄 **Backend Foundations** 與 **Agent Loop Engineering** 的核心觀念、架構設計、最佳實踐、常考 Q&A 與實務踩坑經驗。

---

## 📂 筆記目錄

- [📌 主題一：FastAPI 同步 (Sync) 與非同步 (Async) 核心架構與併發機制](#-主題一fastapi-同步-sync-與非同步-async-核心架構與併發機制)
- [📌 主題二：Clean Architecture 三層架構與 Exception Bubbling 防火牆](#-主題二clean-architecture-三層架構與-exception-bubbling-防火牆)
- [📌 主題三：SQLAlchemy ORM 機制、Alembic 與測試環境建構](#-主題三sqlalchemy-orm-機制alembic-與測試環境建構)
- [📌 主題四：ORM N+1 災難診斷與 Eager Loading 加載模式對比](#-主題四orm-n1-災難診斷與-eager-loading-加載模式對比)
- [📌 主題五：底層架構專題 (B+Tree 索引、MVCC 併發與 Connection Pool)](#-主題五底層架構專題-btree-索引mvcc-併發與-connection-pool)

---

## 📌 主題一：FastAPI 同步 (Sync) 與非同步 (Async) 核心架構與併發機制

### Q1: FastAPI 的 `async def` 與一般 `def` 在底層執行位置有何不同？
- **`async def`**：直接運行在 **主幹道（Event Loop / 事件迴圈）** 上。
  - 只有一個主要的 Thread（單執行緒）。
  - 適用於支援 `async/await` 的非阻塞 I/O（如 `httpx`、`asyncpg`）。
- **一般 `def`**：FastAPI 會自動將其委派到 **服務區（ThreadPool / 背景執行緒池）** 去執行。
  - 當遇到同步阻塞程式碼（如 `time.sleep()`、`requests`）時，會卡在 Worker Thread，**不會阻塞主幹道的 Event Loop**。

---

### Q2: 在 `async def` 裡面寫了同步阻塞程式碼（例如 `time.sleep(5)` 或 `requests.get()`）會怎樣？
- **致命嚴重後果**：
  - 因為 `async def` 是直接在單一主幹道 (Event Loop) 上執行，如果裡面沒有使用非阻塞的 `await` 讓出 CPU 控制權，**整條主幹道會被硬生生卡死 5 秒**。
  - 這 5 秒內，全伺服器所有其他使用者的 Request（哪怕只需要 0.001 秒的 API）全部無法處理，造成整台服務假死！

---

### Q3: 執行 `await` 時，程式會切換到其他的 Thread 嗎？
- **不會！**
- `await` 的本質是 **「合作式多工 (Cooperative Multitasking)」**，完全沒有切換 Thread，依然在**同一個主執行緒 (Main Thread)** 上。
- 當遇到 `await` 時，主執行緒發出非同步請求後主動「讓出控制權（Yield）」，轉頭去處理待辦清單 (Event Loop Queue) 中的其他 Request；等到外部設備（網路/硬碟/DB）回應時，主執行緒再抽空接手繼續執行。

---

### Q4: 如果我全部都用 `async + await`，是不是就可以完全取代 Thread Pool？
- **無法完全取代！**
- 因為 `async/await` 只能解決 **I/O 密集型 (I/O-Bound)** 的等待問題。
- 對於 **CPU 密集型 (CPU-Bound)** 計算（例如：圖片處理、PDF 產生、Pandas 大資料計算），因為計算過程沒有任何 `await` 點可供切換，CPU 會一直處於滿載運算狀態，依然會把主幹道卡死。這種任務必須透過 Thread Pool 或 Process Pool / Celery 來處理解耦。

---

### Q5: 當我呼叫一般 `def` 的 API 時，Thread Pool 到底是什麼時候插進來執行的？
1. **外包任務**：主幹道接到 `def` 請求的第 1 毫秒內，將任務打包丟給背景的 Worker Thread (例如 `Thread-1`)，主幹道隨即恢復自由身繼續接待下一個 Request。
2. **OS 時間切片 (Time-Slicing)**：作業系統在微秒等級內，快速在 Main Thread 與各個 Worker Threads 之間切換 CPU 執行時間。
3. **完成通知**：`Thread-1` 算完後，向主幹道的 Event Loop 發送 Signal，主幹道在空閒時取出結果並 Response 給客戶端。

---

## 📌 主題二：Clean Architecture 三層架構與 Exception Bubbling 防火牆

### 1. 為什麼 Service 層不可以直接 `raise HTTPException(status_code=404)`？
- **解答**：因為 `HTTPException` 是 FastAPI / Starlette 的 Web 框架元件。如果 Service 層出現 HTTP 觀念，當這套商業邏輯未來被移植到 CLI 命令行工具、Celery 背景任務、或者 WebSocket 服務時，就會強綁定 Web 框架，無法獨立運作與測試。
- **最佳實踐**：Service 層只拋出自訂的 Domain Exception（如 `ItemNotFoundError`），由最外層的 FastAPI `app.exception_handler` 統一攔截並轉換為 `JSONResponse`。

---

### 2. 全域異常處理器與 Exception Bubbling（錯誤向上傳遞）
- **解答**：當 Service 層或 Repository 層拋出 Exception 時，因為 Router 層沒有寫 `try...except` 吞掉，Python 的機制會讓錯誤自動向外層呼叫堆疊傳遞 (Bubbling)，最終被最外層 FastAPI 的 `Global Exception Handler` 捕捉，實現優雅的錯誤攔截與轉換。

---

## 📌 主題三：SQLAlchemy ORM 機制、Alembic 與測試環境建構

### 1. Alembic 與資料庫動態配置
- **`sqlalchemy.url` 動態注入**：在 `env.py` 中寫入 `config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)`，可以使用 Pydantic Settings 從環境變數動態取代 `alembic.ini` 中的網址，實現零改動切換 SQLite / PostgreSQL。

---

### 2. SQLAlchemy ORM 運轉與 DTO 防火牆
- **Class vs Instance**：`db.query(TaskModel)` 傳入類別（Table）；`db.add(task_obj)` 傳入物件實例（Row）。
- **Dirty Tracking (自動髒資料追蹤)**：持久化物件在修改屬性後呼叫 `db.commit()`，SQLAlchemy 會自動比對快照並發送 `UPDATE` SQL，無需呼叫 `db.update()`。
- **DTO 轉換**：`TaskModel` 轉為 `TaskResponse` 作為邊界防火牆，避免 DB 欄位異動直接破壞前端 API 介面。

---

### 3. SQLite 記憶體測試 (`sqlite:///:memory:`) 與 `StaticPool`
- **`StaticPool`**：SQLite 記憶體資料庫的生命週期綁定實體連線。測試時必須配置 `poolclass=StaticPool` 避免不同查詢建立新連線導致 `no such table` 錯誤。
- **`check_same_thread=False`**：允許 FastAPI TestClient 在背景 Worker Thread 中安全調用主執行緒建立的 SQLite 記憶體連線。

---

## 📌 主題四：ORM N+1 災難診斷與 Eager Loading 加載模式對比

### 1. 什麼是 N+1 災難？
- **定義**：當使用 ORM 讀取主表資料（1 次 SQL），並在迴圈中存取關聯子表屬性時，ORM 在背景自動觸發 N 次額外 SQL 查詢，導致總查詢次數高達 **$1 + N$ 次**。
- **觸發條件**：存取 ORM 的關聯屬性（如 `user.tasks` 或 `order.items`）。若只讀取主表欄位（如 `user.name`），則完全不會觸發子查詢。

---

### 2. 三大 ORM 加載模式對比

| 加載模式 (Loading Strategy) | 語法 | 發送 SQL 筆數 | 底層機制 | 適用場景 |
| :--- | :--- | :--- | :--- | :--- |
| **Lazy Loading (預設)** | `session.query(UserModel)` | **1 + N 次** | 存取 `user.tasks` 屬性微秒間發送 1 次 `SELECT` | 只處理單一物件時 |
| **`selectinload` ⭐** | `.options(selectinload(User.tasks))` | **精準 2 次** | 1 次查主表，1 次用 `WHERE user_id IN (...)` 批量查 | **一對多 (1-to-Many) / 多對多 (Many-to-Many) 首選** |
| **`joinedload`** | `.options(joinedload(User.tasks))` | **精準 1 次** | 1 次大 `LEFT OUTER JOIN` 查詢 | **多對一 (Many-to-1) / 一對一 (1-to-1)** |

---

### 3. 底層表格與數據對比：為什麼「一對多」首選 IN (`selectinload`) 而不是 JOIN (`joinedload`)？

#### 情境：1 筆訂單 (Order #1) 買了 3 樣商品（鍵盤、滑鼠、螢幕）

#### ❌ 使用 JOIN (`joinedload`) 產生的結果（1 條 SQL，資料重複/膨脹）：
```sql
SELECT orders.id, orders.customer_name, items.item_name, items.price
FROM orders LEFT JOIN items ON orders.id = items.order_id WHERE orders.id = 1;
```
| orders.id | orders.customer_name | items.item_name | items.price |
| :--- | :--- | :--- | :--- |
| 1 | Alice (重複傳送) | 鍵盤 | 1000 |
| 1 | Alice (重複傳送) | 滑鼠 | 500 |
| 1 | Alice (重複傳送) | 螢幕 | 3500 |
> ⚠️ **問題**：`Alice` 和訂單基本資訊被迫在網路上重複傳送了 3 次！在「一對多」買了 100 樣商品時，訂單資訊會重複 100 次，引發嚴重網路頻寬浪費與數據冗餘。

#### ✅ 使用 IN (`selectinload`) 產生的結果（2 條 SQL，資料完全零重複）：
- **第 1 條 SQL**：`SELECT id, customer_name FROM orders WHERE id = 1;` ➡️ **Alice 只傳 1 次**。
- **第 2 條 SQL**：`SELECT id, order_id, item_name, price FROM items WHERE order_id IN (1);` ➡️ **3 樣商品各傳 1 次**。
> ✨ **優勢**：兩邊資料完全不重複傳送，由 ORM 在 Python 記憶體中自動完成物件拼裝！

---

### 4. `joinedload` 的 `.unique()` 陷阱
- **為什麼 `joinedload` 處理一對多時需要 `.unique()`？**
  因為底層 `LEFT JOIN` 的表格列數膨脹（1 個 Alice 對應 3 行 Row）。ORM 必須在記憶體中根據 Primary Key 做去重與折疊，否則 Python `list` 長度會從 2 膨脹成 4，導致 `for user in users:` 迴圈重複執行多次！
- **SQLAlchemy 2.0+ 強制安全機制**：若對一對多使用 `joinedload` 但未呼叫 `.unique()`，會直接拋出 `InvalidRequestError` 崩潰，防止產生業務計數 Bug。
- **為什麼 `selectinload` 不需要 `.unique()`？**
  因為 `selectinload` 的第一條 SQL 是 `SELECT * FROM users`，撈出來的主表物件列表本來就完全獨立不重複！

---

## 📌 主題五：底層架構專題 (B+Tree 索引、MVCC 併發與 Connection Pool)

### 5.1 PostgreSQL 索引機制與 B+Tree 數據結構
- **Hash Index**：尋找 $O(1)$ 最快，但不支援範圍查詢（`WHERE age > 20`）或排序（`ORDER BY`）。
- **B+Tree 樹高與 Fan-out**：一節點可包含數百個 Key/Pointer，1000萬筆資料樹高僅 3~4 層（僅需 3~4 次 Disk I/O）。所有 Data 存於 Leaf Node 且有雙向鏈表，範圍掃描極速完成。
- **Scan 類型**：`Seq Scan` (全表掃描) vs `Index Scan` (走 B+Tree 索引，再回表 Heap Fetch) vs `Index Only Scan` (覆蓋索引 Covering Index 免回表)。

---

### 5.2 PostgreSQL MVCC 多版本併發控制與 Transaction 死鎖
- **MVCC (Multi-Version Concurrency Control)**：寫入/更新時不直接覆蓋舊資料，而是產生帶有 `xmin` 與 `xmax` 的新版本 Row。讀取者根據 Snapshot Transaction ID 只讀可見版本。實現**「讀不阻塞寫，寫不阻塞讀」**！
- **Savepoint 局部回滾 (`db.begin_nested()`)**：在巨量資料批次處理中，利用 Savepoint 做區域性撤銷，防止單一無效資料導致整個大型交易做白工。

---

### 5.3 FastAPI Async Event Loop 與 DB Connection Pool
- **Event Loop 單執行緒機制**：`asyncio` 事件迴圈透過合作式多工 (`await`) 處理高併發 I/O。在 `async def` 中呼叫同步阻塞 DB Driver（如 `psycopg2`）會把整個 Event Loop 釘死！
- **Connection Pool**：SQLAlchemy `QueuePool` (如 `pool_size=10, max_overflow=20`) 複用 TCP 連線，省去每次請求重複三次握手與 Postgres 身份認證開銷。
