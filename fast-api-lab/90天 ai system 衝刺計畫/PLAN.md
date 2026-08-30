<aside>
<img src="i" alt="i" width="40px" />

本計畫專為 **Backend Foundations & AI Agent Systems Engineering** 打造；聚焦高可用後端工程化能力與不依賴框架的 AI Agent 實務。
目標：達標 **台積電 IT / 一線軟體廠 Backend & AI Agent Systems Engineer** 技術面試等級（超越 CRUD，精通系統底層、高併發穩定性與架構決策）。

*(註：C++ 與 LeetCode 演算法已獨立為專屬的 2 個月衝刺計畫 `LEETCODE_CPP_PLAN.md`，不再混於本計畫中)*

</aside>

## 0) 執行規則與時間分配（不可違反）

- **每週總時間：18 小時**（含固定 **3 小時緩衝/除錯**）。
- **其餘 15 小時雙主線比例**：
    1. **Backend Foundations & Production Systems**：**9.0 h（60%）**
    2. **AI Agent Loop Engineering**：**6.0 h（40%）**
- **已完成進度保持（不重算）**：
    - ✅ Ex-01 ~ Ex-06 (Month 1 全部後端與 Agent 基礎任務已 100% 完成)
    - ✅ Ex-07 (Week 7 Agent DAG 與循環依賴驗證已提前完成)
    - 🔄 **原 C++ & OS 軌道已完整獨立移至 `LEETCODE_CPP_PLAN.md`**，本計畫專注於 Backend 與 Agent。
- **進度落後處理順序**：
    1. 先刪 Optional 任務  
    2. 縮小功能規模（scope down）  
    3. **不得犧牲測試與核心交付成果**  
- **Days 85–90 只做**：未完成 High Priority / 測試修復 / README / Demo 準備 / GitHub & 履歷清理；**不得新增新功能**。

---

## 0.1) 核心學習原則：四維底層架構學習法 (Deep Learning Methodology)

> **⚠️ 拒絕做「只會複製貼上程式碼的 CRUD Boy」**
> 本計畫所有主題與練習，AI 與學習者必須嚴格遵守 **「四維底層架構教學模組」**。不只是把 Code 做出來，更要理解程式碼背後的底層機制與架構決策：

1. **今天的主題與核心目標 (Today's Core Topic & Goal)**
   - 清楚定義今天要解決的核心工程問題是什麼。
2. **多種作法的比較與選擇 (Trade-offs & Alternative Comparison)**
   - 比較「傳統作法 vs 現代作法」、「方案 A vs 方案 B」（例如：Raw SQL vs ORM、Lazy Loading vs Eager Loading、Polling vs Event-Driven）。
   - 說明各自的優缺點、時間/空間複雜度與適用場景。
3. **底層運作邏輯與原理 (Underlying Mechanics & Internal Logic)**
   - 拆解背後的作業系統、資料庫或語言機制（例如：PostgreSQL B+Tree 索引、Disk I/O 頁面、MVCC 隔離級別、Python Asyncio Event Loop、Memory Address Pointer）。
4. **常見陷阱避坑與最佳實踐 (Gotchas, Failures & Best Practices)**
   - 分析生產環境中最容易踩坑的地方（例如：N+1 查詢問題、Connection Pool 爆掉、Deadlock 死鎖、Race Condition 競態條件）。

---

## 0.2) 雙檔協作與每日學習 SOP (How PLAN & EXERCISES Work Together)

本衝刺計畫由兩個檔案相互搭配運作，請嚴格遵守以下分工與每日學習 4 步驟：

```
🗺️ PLAN.md (導航儀 & 週地圖)       📖 EXERCISES.md (作業本 & 實驗指導書)      🎯 TSMC面試必考.md (主題式必考題庫)
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│ • 本週大單元與學習目標     │ ➡️   │ • 細項題目 (Ex-1.1 ~ Ex-12.2)│ ➡️   │ • 按主題分門別類歸檔      │
│ • 時數分配 (18h/週)       │      │ • 實作任務與測試交付條件   │      │ • 詳細 Q&A + 底層機制解析 │
│ • 🎯 底層必考原理導讀     │      │ • 💡 大廠面試深挖必考題   │      │ • 專案程式碼/Lab 跳轉連結 │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

### 📅 每日學習 4 步驟 SOP
1. **開工定位（看 PLAN.md）**：打開 [PLAN.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90%E5%A4%A9%20ai%20system%20%E8%A1%9D%E5%88%BA%E8%A8%88%E7%95%AB/PLAN.md)，確認當前週次（如 Week 6）與今天的技術大單元。
2. **領取題目（看 EXERCISES.md）**：打開 [EXERCISES.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90%E5%A4%A9%20ai%20system%20%E8%A1%9D%E5%88%BA%E8%A8%88%E7%95%AB/EXERCISES.md)，找到對應的細項題目（如 【Ex-6.1】），閱讀「📌 實作任務」、「🎯 底層原理」與「💡 大廠面試必考題」。
3. **與 AI 提問學習與實作**：發送指令讓 AI 先解說底層原理與解答面試必考題，再開始撰寫 Code 與單元測試。
4. **打勾驗證與更新狀態**：完成 pytest 測試後，至 [EXERCISES.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90%E5%A4%A9%20ai%20system%20%E8%A1%9D%E5%88%BA%E8%A8%88%E7%95%AB/EXERCISES.md) 更新狀態為 `✅ 已完成`；當該週所有細項題目完成時，至 [PLAN.md](file:///home/wmlab/backend-foundations-lab/fast-api-lab/90%E5%A4%A9%20ai%20system%20%E8%A1%9D%E5%88%BA%E8%A8%88%E7%95%AB/PLAN.md) 勾選週次進度！

---

## 1) 職涯目標

### 目標職位
1. **AI Systems Engineer / AI Agent Engineer**
2. **AI Backend Engineer / Production Systems Engineer (TSMC IT / Top-tier Tech Companies)**

### 核心交付與檢驗能力（台積電 IT / 一線廠面試必考能力清單）
- **高可用後端基建**：FastAPI 異步架構 + Pydantic + 三層 Clean Architecture 解耦。
- **資料庫調優與高併發**：PostgreSQL 資料庫設計、Alembic 遷移、B+Tree 索引效能 (`EXPLAIN ANALYZE`)、MVCC 事務隔離與 Deadlock 防禦。
- **企業級 AI Agent 工作流引擎**：不依賴第三方重型框架，自研具備「結構化輸出驗證 (Pydantic)、DAG 依賴拓撲排程、pgvector 向量檢索 (RAG)、自我修復 (Self-Healing Retry Loop)」之 Agent Controller。
- **穩定性與防禦機制**：分散式追蹤 (Correlation ID)、Token Bucket 限流防禦、Circuit Breaker 熔斷器、Redis Cache-Aside 快取與 DB Connection Pool 調優。
- **現代化雲原生 DevOps**：Linux Namespaces/Cgroups 底層隔離、Multi-stage Dockerfile、Docker Compose 內部 DNS 網絡與 GitHub Actions 冪等 CI/CD Pipeline。

---

## 2) 雙主線專案與交付物（Deliverables）

### Track A：backend-foundations-lab (Task Management REST API)
- **核心架構**：FastAPI + Pydantic + PostgreSQL + SQLAlchemy + Alembic + Docker + GitHub Actions
- **交付物**：Production-ready RESTful API、完整 API 測試 suite (Coverage > 85%)、Docker Compose 配置檔。

### Track B：agent-workflow-lab (Enterprise AI TaskPlan & RAG Agent)
- **核心架構**：Gemini / OpenRouter API + Pydantic Schema + DFS 循環依賴檢測 + pgvector 向量檢索 + Structured Feedback Retry Loop
- **交付物**：不依賴框架的自研 Agent Loop、Benchmark 測試集 (30+ 測試案例)、評估報告 (Evaluation Report)。

---

## 3) 90 天週次規劃表 (Backend & Agent Focused — 含底層必考點)

### 🟢 Month 1：後端基礎與 Agent 核心（Weeks 1–4）

> **【當前狀態】後端與 Agent 軌道已 100% 完成 (Ex-01 ~ Ex-06，25 個測試全過)。**

- **Backend (✅ 已完成)**: Python 基礎、Context Manager (資源生命週期)、Exception Bubbling、JSON Validator、Task REST API v0.1 (Router-Service-Repository 三層解耦與依賴注入)。
- **Agent (✅ 已完成)**: TaskPlan Schema (Pydantic 限制)、Gemini Tool Parser (inspect 解析內省)、Generate-Validate-Retry Agent Loop (Structured Feedback Loop)。

---

### 🟡 Month 2：PostgreSQL 資料庫、向量檢索與高級驗證（Weeks 5–8）

#### Week 5：SQL 實戰與 PostgreSQL 整合（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: 建立 Users/Projects/Tasks Schema，撰寫手寫 SQL 與 PostgreSQL Integration Test。
  - **【🎯 底層必考原理與學習重點】**:
    1. **SQL 邏輯執行順序 (Execution Order)**：`FROM` ➡️ `ON` ➡️ `JOIN` ➡️ `WHERE` ➡️ `GROUP BY` ➡️ `HAVING` ➡️ `SELECT` ➡️ `DISTINCT` ➡️ `ORDER BY` ➡️ `LIMIT`（明白為什麼 `WHERE` 不能直接使用 `SELECT` 的別名 alias）。
    2. **Primary Key vs Foreign Key 限制原理**：B+Tree Unique Constraint 檢查機制與參照完整性 (Referential Integrity) 級聯鎖定 (`ON DELETE CASCADE`)。
    3. **ACID 特性**：Atomicity (原子性)、Consistency (一致性)、Isolation (隔離性)、Durability (持久性/WAL 日誌)。
- **Agent (6.0h)**:
  - **【實作任務】**: Prompt Versioning 機制與記錄每次 Agent Run 的 Raw IO 日誌持久化。
  - **【🎯 底層必考原理與學習重點】**:
    1. **LLM 呼叫的可追溯性 (Observability)**：非確定性 (Non-deterministic) 系統的測試困境與 Prompt 覆點紀錄。
- **緩衝 (3.0h)**: 進度除錯與重構

#### Week 6：SQLAlchemy ORM 與 Alembic Migration（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: SQLAlchemy ORM Models 定義、Repository 層改寫、Alembic 遷移與 Transaction Rollback 測試 (Ex-08 完成)。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Unit of Work 模式與 Identity Map**：SQLAlchemy Session 如何透過內建字典維護記憶體中的物件狀態（Transient ➡️ Pending ➡️ Persistent ➡️ Detached）。
    2. **Dirty Tracking 機制**：為何不需要呼叫 `db.update()`？Session 在 `flush()` 時會比對原始 Snapshot 與當前屬性自動生成 `UPDATE` SQL。
    3. **Alembic 遷移原理**：以 Hash 雙向鏈表管理版本 Revision，對比 `Base.metadata` 與 DB `information_schema` 生成 `upgrade()` 與 `downgrade()` 腳本。
    4. **Transaction Savepoint 與 Rollback**：當中途發生 Exception 時，如何透過 `db.rollback()` 釋放資料庫連線與 Undo Log，防止連線被污染。
- **Agent (6.0h)**:
  - **【實作任務】**: Semantic Validator 語意檢查模組實作與精準修復 Prompt 生成。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Structured Feedback 閉環控制**：將 `ValidationError` 的 `loc` (錯誤位置) 與 `msg` (錯誤原因) 精準轉化為 LLM 修正提示，降低 80% 無用重試成本。
- **緩衝 (3.0h)**: 進度補齊與單元測試

#### Week 7：資料庫調優、pgvector 檢索與圖論 DAG（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: Pagination & Filtering、B+Tree Index 測試與 EXPLAIN ANALYZE 效能診斷 (Ex-09 完成)。
  - **【🎯 底層必考原理與學習重點】**:
    1. **B+Tree 數據結構與 Disk I/O 頁面**：扇出 (Fan-out) 效應、樹高 3~4 層特性、與 Hash Index (無 Range Query) 及紅黑樹 (樹太高 I/O 太多) 的比較。
    2. **N+1 查詢問題與三種 SQL 加載模式**：`joinedload` (JOIN 一次拿，有笛卡兒積風險) vs `selectinload` (`WHERE id IN (...)` 拆二次，最推薦) vs `subqueryload`。
    3. **Composite Index（複合索引）最左字首原則 (Leftmost Prefix Rule)**：建立 `(status, created_at)` 索引時，為何 `WHERE created_at = ?` 無法命中索引。
    4. **EXPLAIN ANALYZE 診斷**：判讀 `Seq Scan` (全表掃描)、`Index Scan` (回表 Heap Fetch) 與 `Index Only Scan` (Covering Index 免回表)。
- **Agent (6.0h - ✅ Ex-07 已完成)**:
  - **【實作任務】**: DAG 有向無環圖依賴建立與 DFS 循環依賴檢測；整合 PostgreSQL `pgvector` 進行 Tool/Doc 相似度檢索。
  - **【🎯 底層必考原理與學習重點】**:
    1. **圖論 DFS 三色標記法 (White/Gray/Black)**：白色(未造訪)、灰色(當前遞迴路徑中)、黑色(已造訪完成)。當 DFS 遇到灰色節點即代表存在環路 (Back Edge)。
    2. **RAG 向量檢索原理 (pgvector)**：餘弦相似度 (Cosine Distance) 與 HNSW (Hierarchical Navigable Small World) / IVFFlat 向量索引原理。
- **緩衝 (3.0h)**: 雙週技術總結

#### Week 8：Month 2 整合、非同步排程與分散式日誌（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: AppConfig 環境變數解耦、Request Correlation ID 中間件、Token Bucket 限流防禦與 Structured JSON Logging。
  - **【🎯 底層必考原理與學習重點】**:
    1. **12-Factor App 理念**：組態 (Config) 嚴格從環境變數注入 (`pydantic-settings`)，做到 Code 與 Config 徹底解耦。
    2. **Middleware 的 Request/Response 生命週期**：FastAPI / Starlette 洋蔥圈模型 (Onion Model)，例外處理與 Context Variable 傳遞。
    3. **Request Correlation ID (Trace ID)**：分散式系統中跨服務追蹤日誌的核心，將 UUID 綁定至 `ContextVar` 並印入每一行 JSON 日誌。
    4. **Rate Limiting 限流演算法**：Token Bucket (令牌桶) vs Leaky Bucket (漏桶)，在高併發下保護後端服務與 LLM API Token 預算。
- **Agent (6.0h)**:
  - **【實作任務】**: 整合 Generate ➡️ Validate ➡️ Feedback ➡️ Retry 全流程 Agent Loop，跑 20 個 Benchmark 測試集。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Agent 評估維度 (Evaluation Metrics)**：Schema Pass Rate (格式通過率)、First-Attempt Pass Rate (一次通過率)、Average Token Cost 與 Latency。
- **緩衝 (3.0h)**: Month 2 Gate 技術驗收

---

### 🟠 Month 3：Docker、CI/CD、系統設計與面試準備（Weeks 9–12）

#### Week 9：Docker 容器化與服務整合（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: 多階段編譯 (Multi-stage Build) Dockerfile、Docker Compose 整合 API + PostgreSQL 服務。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Linux 容器底層隔離機制**：**Namespaces** (PID/NET/IPC/MNT 資源視覺隔離) 與 **Cgroups** (CPU/RAM 硬體資源上限限制)。
    2. **Docker 鏡像層級快取 (Layer Caching)**：為何 `COPY requirements.txt` 要放在 `COPY . .` 之前？極大化加速 build 過程。
    3. **Docker Compose Bridge 網路與 Internal DNS**：容器間如何透過 Service Name (如 `db:5432`) 進行內部通信與 DNS 剖析。
- **Agent (6.0h)**:
  - **【實作任務】**: Metric Collector (記錄 Latency, Token Cost, Retry Times) 並產出 Evaluation JSON 報告。
  - **【🎯 底層必考原理與學習重點】**:
    1. **LLM API 的收斂性分析**：分析 Retry 次數上限與 Token 邊際效益遞減點。
- **緩衝 (3.0h)**: Docker Compose 排錯

#### Week 10：GitHub Actions CI/CD 自動化（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: GitHub Actions Workflow (.github/workflows/ci.yml)、PostgreSQL Service Containers、Ruff/Mypy 檢查。
  - **【🎯 底層必考原理與學習重點】**:
    1. **CI Pipeline 冪等性 (Idempotency)**：確保任何 PR 觸發的 CI 環境都是乾淨且可重複驗證的（Ephemeral Container）。
    2. **靜態型別檢查 (Mypy) 與 Linter (Ruff)**：編譯期/檢查期發現 Python 動態型別潛在 Bug（如 `Optional[T]` 未判斷 `None` 的 AttributeError）。
- **Agent (6.0h)**:
  - **【實作任務】**: Agent Evaluation Report 撰寫與 Benchmark 成果視覺化。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Benchmark 防劇透與防過擬合 (Overfitting)**：確保測試集包含極端極限邊界案例 (Edge Cases)。
- **緩衝 (3.0h)**: CI 流程補強

#### Week 11：高併發系統設計、快取與高可用防禦（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: 完善專案 README.md、Redis 快取整合 (Cache-Aside)、Circuit Breaker 熔斷器與 DB Connection Pool 調優。
  - **【🎯 底層必考原理與學習重點】**:
    1. **快取策略 (Caching Strategies)**：**Cache-Aside** vs **Write-Through**；快取穿透 (Bloom Filter)、擊穿 (Mutex Lock)、雪崩 (Random Jitter) 防禦。
    2. **Redis 底層與記憶體淘汰策略**：單執行緒 Reactor 模式、LRU vs LFU 淘汰演算法。
    3. **Circuit Breaker (熔斷器模式)**：Closed ➡️ Open ➡️ Half-Open 三態狀態機，防止下游 LLM/DB 崩潰引發連鎖雪崩。
    4. **Load Balancing 演算法**：Round-Robin、Least Connections、Consistent Hashing (一致性 Hash)。
- **Agent (6.0h)**:
  - **【實作任務】**: 擴充 Agent Benchmark 至 30 個測試情境，錄製/撰寫 Demo 與系統限制說明。
  - **【🎯 底層必考原理與學習重點】**:
    1. **Agent 的死角與限制**：明確說明死迴圈 (Infinite Loop) 防禦與 Context Window 長度限制對策。
- **緩衝 (3.0h)**: 系統設計問答演練

#### Week 12：技術面試演練與最終驗收（18h）
- **Backend (9.0h)**:
  - **【實作任務】**: 限時無 AI 白板手寫小型帶 DB API、模擬後端技術問答、履歷精修。
  - **【🎯 底層必考原理與學習重點】**:
    1. **台積電 IT / 一線廠高頻必考問答攻防**：
       - SQL B+Tree 索引細節與 N+1 解法。
       - ACID 與 MVCC 隔離級別（髒讀、不可重複讀、幻讀、Deadlock 解決）。
       - Python Asyncio Event Loop 與 GIL (Global Interpreter Lock) 對 CPU-bound vs I/O-bound 的影響。
       - Circuit Breaker 熔斷與 Rate Limiting 令牌桶機制。
- **Agent (6.0h)**:
  - **【實作任務】**: 模擬 AI/Agent Engineer 技術面試問答 (Structured Output, Validation, Retry, Evaluation, pgvector RAG)。
  - **【🎯 底層必考原理與學習重點】**:
    1. **自研 Agent 核心優勢說明**：為什麼不使用 LangChain？(解決黑盒問題、追蹤 Latency/Cost、精準操控 Control Flow)。
- **緩衝 (3.0h)**: 全套模擬面試演練

---

### 🔴 Days 85–90：最終緩衝（Final Buffer）

- 專注處理：
  1. GitHub Repositories 整理與 README 優化。
  2. 履歷投遞與自我介紹演練。
  3. 絕對不新增任何新功能。

---

## 4) 每週與每月檢查機制 (Definition of Done)

### 每週檢查點 (Weekly DoD)
- **週五/週六檢討**：核對本週雙主線進度完成度。
- **時數控管**：確認未超過 18 小時上限；若落後則使用 3 小時緩衝時間。

### 每月 Gate 驗收標準 (Monthly Gate — 台積電 IT / 一線廠標準)
- **Month 1 Gate (✅ 通過)**：無 AI 獨立寫出三層架構 REST API，測試覆蓋完整；Agent 基礎 Retry 通過。
- **Month 2 Gate**：PostgreSQL Migration 與 CRUD 正常運作；能清晰解釋 B+Tree 索引、N+1 查詢解法、MVCC 併發與 pgvector 向量檢索；Agent DAG 循環依賴檢測 100% 正確。
- **Month 3 Gate**：Docker Compose 與 GitHub Actions CI 綠燈；能回答系統設計 (Caching/Circuit Breaker/Rate Limiter/DB Pool) 與 Agent Benchmark 報告產出。
