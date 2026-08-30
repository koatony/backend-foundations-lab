# TSMC / 一線大廠 Backend & AI System Engineering 面試必考題庫

本文件為專屬 **TSMC IT / 一線廠 Backend System & DB Infrastructure** 的面試必考題庫。
所有題目均依據 **技術主題分門別類** 歸檔，後續新增題目時必須先審視分類並插入對應主題下，禁止直接堆疊於檔案末端。

---

## 📂 題目主題索引

- [📌 主題一：資料庫與物理 I/O 調優 (Database & Disk I/O)](#-主題一資料庫與物理-io-調優-database--disk-io)
  - [題 1.1: Covering Index 覆蓋索引與 Random I/O 回表診斷](#題-11-covering-index-覆蓋索引與-random-io-回表診斷)
  - [題 1.2: 深度分頁 (`LIMIT / OFFSET`) 物理瓶頸與 Deferred Join 解法](#題-12-深度分頁-limit--offset-物理瓶頸與-deferred-join-解法)
  - [題 1.3: 交易原子性、保存點 (`SAVEPOINT`) 與局部隔離回滾機制](#題-13-交易原子性保存點-savepoint-與局部隔離回滾機制)
  - [題 1.4: ORM N+1 災難診斷、`selectinload` vs `joinedload` 機制與面試攻防](#題-14-orm-n1-災難診斷selectinload-vs-joinedload-機制與面試攻防)
- [📌 主題二：高併發、OS 系統調用與持久化寫入 (High Concurrency & OS Syscalls)](#-主題二高併發os-系統調用與持久化寫入-high-concurrency--os-syscalls)
  - [題 2.1: 高併發寫入瓶頸、WAL 刷盤與 `fsync()` 系統調用開銷](#題-21-高併發寫入瓶頸wal-刷盤與-fsync-系統調用開銷)
- [📌 主題三：Python 高級語言特性與異步併發 (Python Core & Async)](#-主題三python-高級語言特性與異步併發-python-core--async)
- [📌 主題四：分佈式系統、快取與微服務防禦 (Distributed Systems & Redis)](#-主題四分佈式系統快取與微服務防禦-distributed-systems--redis)

---

## 📌 主題一：資料庫與物理 I/O 調優 (Database & Disk I/O)

### 題 1.1: Covering Index 覆蓋索引與 Random I/O 回表診斷

#### ❓ 【題目情境】
`users` 表有 1,000 萬筆資料，主鍵為 `id`，我們建立了複合索引：
```sql
CREATE INDEX idx_dept_age ON users(department_id, age);
```
現有以下兩支查詢 API 的 SQL 語句：
- **Query A**: `SELECT id, age FROM users WHERE department_id = 42;`
- **Query B**: `SELECT id, age, name FROM users WHERE department_id = 42;`

1. 請說明 Query A 與 Query B 在 PostgreSQL/MySQL 執行計畫（Execution Plan）上的本質差異。
2. 為什麼 Query B 的執行時間可能比 Query A 慢上十倍以上？
3. 如果在不改變 `SELECT name` 需求的前提下，你會如何修改索引或 SQL 來優化 Query B？

#### 💡 【硬核解答與底層原理】
1. **執行計畫差異**：
   - **Query A**：數據庫會走 **`Index Only Scan` (覆蓋索引)**。因為次級索引 `idx_dept_age` 的 B+Tree 葉子節點中已包含了 `department_id`（索引鍵）、`age`（索引鍵）以及 `id`（隱式主鍵 PK）。查詢所需的全部欄位均可在索引樹直接獲取，**完全不需要存取資料頁 (0 Heap Fetch)**。
   - **Query B**：數據庫會走 **`Index Scan` (回表/Heap Fetch)**。因為 `name` 欄位不在次級索引中，數據庫在索引樹查到符合 `department_id = 42` 的條目後，必須拿著 `id` 回到主鍵 B+Tree 或 Heap 資料頁讀取完整的 Row 才能取得 `name`。
2. **效能差異原因 (Random Read Disk I/O)**：
   - 當符合條件的 Row 數量很大且物理存儲不連續時，Query B 回表會引發大量的**物理隨機 I/O (Random Disk I/O)**。從磁碟讀取資料頁面比單純在記憶體中掃描索引頁面慢幾個數量級。
3. **優化方案**：
   - **方案 A (Covering Index)**：擴充複合索引或使用 `INCLUDE` 語句（PostgreSQL 11+），將 `name` 納入索引：
     ```sql
     -- 方法 1：傳統複合索引
     CREATE INDEX idx_dept_age_name ON users(department_id, age, name);
     
     -- 方法 2：Postgres INCLUDE 覆蓋索引 (name 只存於葉子節點，不參與 B+Tree 樹枝排序)
     CREATE INDEX idx_dept_age_inc ON users(department_id, age) INCLUDE (name);
     ```
     改動後 Query B 將轉為 `Index Only Scan`，免去回表隨機 I/O。

#### 🔗 【專案對應與實作連結】
- **所屬模組**：Module 7 (Ex-7.1)
- **實作/對應檔案**：[EXERCISES.md (Ex-7.1)](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/EXERCISES.md#L218)
- **專案狀態**：⏳ 進行中（測試腳本規劃於 `fast-api-lab/scripts/explain_analysis.sql`）

---

### 題 1.2: 深度分頁 (`LIMIT / OFFSET`) 物理瓶頸與 Deferred Join 解法

#### ❓ 【題目情境】
社群/電商平台要撈出歷史訂單，前端發起請求：
```sql
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10 OFFSET 1000000;
```
即使在 `created_at` 上建了索引，DBA 依然警告這支 API 會拖垮資料庫。

1. 請從 B+Tree 索引樹結構與「回表（Random I/O）」的角度，解釋為什麼 `OFFSET 1000000` 會極度緩慢？
2. 請給出兩種能避開百萬次無用回表的優化 SQL 寫法。

#### 💡 【硬核解答與底層原理】
1. **效能瓶頸成因**：
   - `OFFSET 1000000 LIMIT 10` 的語意是「跳過前 1,000,000 筆，取第 1,000,001 ~ 1,000,010 筆」。
   - 數據庫引擎必須先掃描並取出前 **1,000,010** 筆資料。由於 `SELECT *` 需要非索引欄位，引擎會對這 1,000,010 筆資料**每一筆都執行一次物理回表 (Heap Fetch)**，完成後再把前 1,000,000 筆拋棄！這造成了 1,000,000 次完全浪費的物理隨機 Disk I/O。
2. **優化寫法**：
   - **解法 1：延遲關聯 (Deferred Join / 覆蓋索引掃描)**：
     先在子查詢中利用索引進行 `Index Only Scan` 找出目標 10 筆的 `id`（免回表），再主查詢回表 10 次獲取 `*`：
     ```sql
     SELECT o.* 
     FROM orders o
     JOIN (
         SELECT id FROM orders ORDER BY created_at DESC LIMIT 10 OFFSET 1000000
     ) AS tmp ON o.id = tmp.id;
     ```
     *效能提升*：回表次數從 **1,000,010 次** 銳減為 **10 次**！
   - **解法 2：游標分頁 (Keyset Pagination / Seek Method)**：
     若前端改為傳遞上一頁最後一筆的 `created_at` 與 `id`：
     ```sql
     SELECT * FROM orders 
     WHERE (created_at, id) < ('2026-08-01 12:00:00', 987654)
     ORDER BY created_at DESC, id DESC 
     LIMIT 10;
     ```
     *效能提升*：直接利用 B+Tree 點查 (B+Tree Search Path) 快速定位，時間複雜度為 $O(\log N)$，徹底消除 `OFFSET` 掃描。

#### 🔗 【專案對應與實作連結】
- **所屬模組**：Module 7 (Ex-7.1 擴充題)
- **實作/對應檔案**：[EXERCISES.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/EXERCISES.md#L218)
- **專案狀態**：目前尚無專屬分頁 Lab (未做)

---

### 題 1.3: 交易原子性、保存點 (`SAVEPOINT`) 與局部隔離回滾機制

#### ❓ 【題目情境】
後端系統要執行一筆包含 1,000 筆訂單的批次匯入作業。若採用整筆交易 (Transaction) 封裝：
1. 若第 500 筆訂單格式錯誤爆出例外，如果不做處理直接全盤 `ROLLBACK`，會有什麼問題？
2. 若改為每筆訂單都發送一次 `COMMIT`，又會引發什麼效能與資料一致性危機？
3. 在 ORM (如 SQLAlchemy) 與 SQL 層，如何利用 **`SAVEPOINT` (保存點)** 實作「局部回滾 (Partial Rollback)」，既保留前 499 筆成功寫入，又不會因為單一錯誤導致整個批次處理白做？

#### 💡 【硬核解答與底層原理】
1. **全盤 ROLLBACK 瓶頸**：
   - 違反吞吐量效益。單一異常導致前 499 筆已驗證無誤的 I/O 工作全部撤銷，必須重新發起整批重試，浪費網路 RTT 與 DB 運算資源。
2. **單筆頻繁 COMMIT 危機**：
   - 每筆 `COMMIT` 均會強制觸發 `fsync()` WAL 刷盤，吞吐量嚴重受限；且若中途斷電崩潰，資料庫會留下部分完成的半成品資料，破壞業務層級的原子性。
3. **SAVEPOINT (局部隔離回滾) 底層機制**：
   - 在 DB 底層，`SAVEPOINT savepoint_name` 會在當前 Transaction 的 Undo Log / WAL 標記一個內部保存標籤。
   - 當第 500 筆爆錯時，執行 `ROLLBACK TO SAVEPOINT savepoint_name`。DB 只會撤銷 Savepoint 之後的變更，而**不會讓整個 DB 連線進入 `Aborted` 失效狀態**。
   - **SQLAlchemy 實作**：呼叫 `savepoint = db.begin_nested()`。當發生 Exception 時於 `except` 區塊執行 `savepoint.rollback()`，處理完畢後最外層再執行 `db.commit()`。

#### 🔗 【專案對應與實作連結】
- **所屬模組**：Module 6 (Ex-6.3)
- **實作/對應檔案**：[EXERCISES.md (Ex-6.3)](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/EXERCISES.md#L205)
- **專案狀態**：✅ 已完成測試驗證（參見 [`tests/repositories/test_task_repositoy_db.py`](file:///home/wmlab/backend-foundations-lab/fast-api-lab/tests/repositories/test_task_repositoy_db.py) 中的 `test_transaction_rollback_on_error` 與 `test_transaction_full_rollback_on_batch_error`）

---

### 題 1.4: ORM N+1 災難診斷、`selectinload` vs `joinedload` 機制與面試攻防

#### ❓ 【題目情境：4 大經典面試攻防題】

##### 1. 電商訂單與商品（程式碼找碴）
```python
orders = session.query(Order).order_by(Order.created_at.desc()).limit(100).all()
result = []
for order in orders:
    item_names = [item.product_name for item in order.items]
    result.append({"order_id": order.id, "items": item_names})
```
- **問題**：這段 code 執行完資料庫收到幾次 SQL 查詢？有無 N+1？如何優化？
- **解答**：收到 **101 次** SQL 查詢（1 次主查詢 + 100 次 `Order.items` 子查詢）。這是典型的 **N+1 災難**。應改用 `.options(selectinload(Order.items))` 將查詢精準降為 **2 次**。

##### 2. 部門與主管（多對一關聯 Many-to-One）
```python
employees = session.query(Employee).all()
for emp in employees:
    print(emp.name, emp.department.name)
```
- **問題**：是否有 N+1？針對多對一，更推薦 `JOIN` (`joinedload`) 還是 `IN` (`selectinload`)？
- **解答**：有 N+1（101 次 SQL）。針對**多對一 (Many-to-One)** 關聯，更推薦 **`JOIN` (`joinedload`)**！因為 1 個員工只屬於 1 個部門，`LEFT JOIN` 不會產生「一對多」的笛卡兒積重複資料，只需 **1 次 SQL** 即可完美撈出。

##### 3. 原生 SQL N+1 效能瓶頸重構
```python
users = db.execute("SELECT id, name FROM users WHERE is_active = 1 LIMIT 100")
user_logins = {}
for user in users:
    log = db.execute(f"SELECT login_time FROM login_logs WHERE user_id = {user['id']} ORDER BY login_time DESC LIMIT 1")
    user_logins[user["id"]] = log
```
- **問題**：效能瓶頸在哪？如何優化成 1~2 條 SQL？
- **解答**：瓶頸在於迴圈內對 DB 進行 100 次網路往返 (RTT)。
  - **解法 A (2 條 SQL - IN 寫法)**：先撈 users，拿 id 清單發送 `SELECT user_id, MAX(login_time) FROM login_logs WHERE user_id IN (1, 2, ..., 100) GROUP BY user_id;`
  - **解法 B (1 條 SQL - Window Function 視窗函數)**：
    ```sql
    WITH ranked_logins AS (
        SELECT user_id, login_time, ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY login_time DESC) as rn
        FROM login_logs
    )
    SELECT u.id, u.name, r.login_time
    FROM users u
    JOIN ranked_logins r ON u.id = r.user_id AND r.rn = 1
    WHERE u.is_active = 1 LIMIT 100;
    ```

##### 4. 陷阱題：沒存取關聯屬性會發送 N+1 嗎？
```python
users = session.query(UserModel).all()
for user in users:
    print(user.name, user.email)
```
- **問題**：這段會引發 N+1 嗎？
- **解答**：**完全不會！** 總共只會發送 **1 次 SQL**（`SELECT * FROM users`）。因為程式碼只讀取了 `UserModel` 自身的欄位（`name` 和 `email`），完全沒有碰觸關聯屬性 `user.tasks`。Lazy Loading 只會在存取關聯屬性的那一微秒才觸發子查詢。

---

#### 💡 【`joinedload` 笛卡兒積與 `.unique()` 記憶體去重機制】

- **`LEFT JOIN` 數據膨脹問題**：
  在「一對多」關聯（如 1 筆 Order 買 3 樣 Item）使用 `joinedload` 時，SQL 會發送 `orders LEFT JOIN items`。資料庫回傳的原始表格中，Order 的 `id` 與 `customer_name` 會被迫在網路上**重複傳送 3 次**。
- **`.unique()` 的作用**：
  ORM 在接收到 `LEFT JOIN` 的扁平表格時，長度膨脹成 4 行 Row。必須加上 `.unique()`，允許 ORM 在 Python 記憶體中根據 Primary Key 做物件去重與關聯折疊，否則 Python `users` 清單長度會從 2 膨脹成 4，導致商業邏輯迴圈重複執行！

#### 🔗 【專案對應與實作連結】
- **所屬模組**：Module 7 (Ex-7.2)
- **實作/對應檔案**：[EXERCISES.md (Ex-7.2)](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/EXERCISES.md#L232)
- **專案狀態**：✅ 已完成測試驗證（參見 [`tests/performance/test_n_plus_one.py`](file:///home/wmlab/backend-foundations-lab/fast-api-lab/tests/performance/test_n_plus_one.py)）

---

## 📌 主題二：高併發、OS 系統調用與持久化寫入 (High Concurrency & OS Syscalls)

### 題 2.1: 高併發寫入瓶頸、WAL 刷盤與 `fsync()` 系統調用開銷

#### ❓ 【題目情境】
日誌/履歷追蹤 API 每秒收到 5,000 筆 Log 寫入請求。後端工程師採用「每收到一筆請求就發起一次 `INSERT INTO logs ...` 且立刻 `COMMIT`」的方式。
結果 Server 的 CPU `sys` 時間與 IO-Wait 飆高，系統 TPS 只能達到 300 左右。

1. 從 OS 系統調用與數據庫 WAL（Write-Ahead Logging）機制來看，為什麼每次 `COMMIT` 發起的 `fsync()` 會造成嚴重的效能瓶頸？
2. 如果要在應用層與資料庫層優化，有哪些架構設計模式或併發處理機制？

#### 💡 【硬核解答與底層原理】
1. **底層瓶頸分析 (`fsync()` 阻塞與刷盤開銷)**：
   - 當事務 `COMMIT` 時，資料庫為了滿足 ACID 中的 D (Durability 持久性)，必須呼叫 POSIX 系統調用 `fsync(fd)`，強迫 OS 將 Kernel Page Cache 中的 WAL 日誌緩衝區物理寫入硬盤。
   - `fsync()` 是一個**阻塞型 (Blocking) 系統調用**。每秒 5,000 次單筆 commit 意味著每秒觸發 5,000 次 CPU 使用者態/核心態切換 (Context Switch) 以及磁碟驅動器同步鎖。物理 SSD/HDD 的隨機 `fsync` 響應延遲約在 1~3ms，導致單線程/單連線吞吐量上限被硬性卡在 300~1000 TPS。
2. **優化架構與設計模式**：
   - **應用層解法：批次寫入 (Batching / Group Commit Pattern)**：
     在 FastAPI/Backend 後端使用記憶體 Ring Buffer / Channel 收集寫入請求，每累積 100 筆或每隔 10ms 批次發起一次 `INSERT INTO logs (col) VALUES (...), (...), ...;`。將 100 次 `fsync()` 攤平 (Amortize) 為 1 次。
   - **資料庫層解法：WAL Group Commit & 異步刷盤**：
     調整資料庫參數（如 PostgreSQL 的 `synchronous_commit = off` 或 MySQL 的 `innodb_flush_log_at_trx_commit = 2`），讓事務 commit 時僅寫入 OS Page Cache，由 DB 背景執行緒每秒統一 `fsync()` 刷盤（以微小的 RPO 數據丟失風險換取十倍吞吐量提升）。

#### 🔗 【專案對應與實作連結】
- **所屬模組**：Module 8 / Module 11 (高併發寫入與中間件)
- **實作/對應檔案**：[EXERCISES.md (Ex-8.4 / Ex-11.3)](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90天%20ai%20system%20衝刺計畫/EXERCISES.md#L34)
- **專案狀態**：目前尚無專屬 fsync Batching Lab (未做)

---

## 📌 主題三：Python 高級語言特性與異步併發 (Python Core & Async)

*(預留主題目錄，後續題目將新增於此)*

---

## 📌 主題四：分佈式系統、快取與微服務防禦 (Distributed Systems & Redis)

*(預留主題目錄，後續題目將新增於此)*
