<aside>
<img src="i" alt="i" width="40px" />

本計畫專為 **台積電 IT (TSMC IT Software/Backend/AI Engineer)** 打造；聚焦高可用後端工程化能力、AI Agent 實務與台積電第一關 HackerRank / LeetCode OA 線上測驗衝刺。

</aside>

## 0) 執行規則與時間分配（不可違反）

- **每週總時間：18 小時**（含固定 **3 小時緩衝/除錯/模擬測驗**）。
- **其餘 15 小時三大軌道比例**：
    1. **Backend Foundations & Production**：**7.5 h（50%）**
    2. **AI Agent Loop Engineering**：**3.75 h（25%）**
    3. **LeetCode & DSA OA 衝刺（台積電 IT 專攻，取代原 C++ 軌道）**：**3.75 h（25%）**
- **已完成進度保持（不重算）**：
    - ✅ Ex-01 ~ Ex-06 (Month 1 全部後端與 Agent 基礎任務已 100% 完成)
    - ✅ Ex-07 (Week 7 Agent DAG 與循環依賴驗證已提前完成)
    - 🔄 **原 C++ 軌道全面替換為台積電 IT LeetCode OA 演算法衝刺**（從第 1 題開始進行高頻題訓練）。
- **進度落後處理順序**：
    1. 先刪 Optional 題目/任務  
    2. 縮小功能規模（scope down）  
    3. **不得犧牲測試與核心交付成果**  
- **Days 85–90 只做**：未完成 High Priority / 測試修復 / README / Demo 準備 / GitHub & 履歷清理；**不得新增新功能**。

---

## 1) 職涯目標：台積電 IT (TSMC IT)

### 目標職位
1. TSMC IT - Software Engineer / Backend Engineer
2. TSMC IT - AI Systems / Agent Application Engineer
3. Python Backend & Production Systems Engineer

### 關卡拆解與核心能力清單
- **第一關：線上程式測驗 (HackerRank / LeetCode OA)**
  - 熟練精通 Array/Hash, Two Pointers, Sliding Window, Stack/Queue, BFS/DFS, Graph (Topological Sort), DP, Binary Search 等經典 Medium 題型。
- **第二關：技術面試 (Production-ready 工程能力)**
  - 獨立撰寫高維護性 RESTful API (FastAPI + Pydantic + 三層架構)。
  - PostgreSQL 資料庫設計、Migration (Alembic)、Indexing 與 Transaction 優化。
  - 完整單元與整合測試 (pytest + Mock + Fixtures + AAA 規範)。
  - Docker 容器化與 Multi-container 部署 (Docker Compose)。
  - CI/CD 自動化流程 (GitHub Actions)。
- **第三關：主管與 AI/主管面試 (AI/Agent 實用落地)**
  - LLM Agent 結構化輸出 (Structured Output) 驗證與重試機制 (Generate-Validate-Retry)。
  - 有向無環圖 (DAG) 任務依賴解析與循環依賴檢測。
  - Agent 評估指標 (Latency, Cost, Accuracy Benchmark)。

---

## 2) 三大軌道專案與交付物（Deliverables）

### Track A：backend-foundations-lab (Task Management REST API)
- **核心架構**：FastAPI + Pydantic + PostgreSQL + SQLAlchemy + Alembic + Docker + GitHub Actions
- **交付物**：Production-ready RESTful API、完整 API 測試 suite (Coverage > 85%)、Docker Compose 配置檔。

### Track B：agent-workflow-lab (AI TaskPlan Agent)
- **核心架構**：Gemini API + Pydantic Schema + DFS 循環依賴檢測 + Structured Feedback Retry Loop
- **交付物**：不依賴框架的自研 Agent Loop、Benchmark 測試集 (30+ 測試案例)、評估報告 (Evaluation Report)。

### Track C：leetcode-oa-lab (台積電 IT HackerRank/LeetCode 衝刺)
- **核心架構**：Python/Modern C++ 雙語解題庫、單元測試驗證、複雜度分析與解題筆記
- **交付物**：精選 45+ 題台積電 IT 高頻 OA 題目（Easy 15 題 / Medium 30 題）、分類整理演算法模板筆記。

---

## 3) 90 天週次與每日任務規劃表

### 🟢 Month 1：後端基礎、Agent 核心與 LeetCode 打底（Weeks 1–4）

> **【當前狀態】後端與 Agent 軌道已 100% 完成 (Ex-01 ~ Ex-06)；本區段專注於 LeetCode 第一階段補齊。**

#### Week 1 ~ Week 4 已完成成果與 LeetCode 補齊：
- **Backend (✅ 已完成)**: Python 基礎、Context Manager、Exception Bubbling、JSON Validator、Task REST API v0.1 (三層架構 + 25 pytest cases)。
- **Agent (✅ 已完成)**: TaskPlan Schema、Gemini Tool Parser、Generate-Validate-Retry Agent Loop (7 pytest cases)。
- **LeetCode 衝刺 (本月新增每日任務)**:
  - **W1 每日標靶**: LeetCode 1. Two Sum (Easy), 217. Contains Duplicate (Easy)
  - **W2 每日標靶**: LeetCode 242. Valid Anagram (Easy), 49. Group Anagrams (Medium)
  - **W3 每日標靶**: LeetCode 121. Best Time to Buy/Sell Stock (Easy), 167. Two Sum II (Medium)
  - **W4 每日標靶**: LeetCode 15. 3Sum (Medium), 11. Container With Most Water (Medium)
  - **Month 1 演算法總結**: 熟悉 Array & Hashing, Two Pointers 核心思考模式。

---

### 🟡 Month 2：PostgreSQL 資料庫、Agent 高級驗證與 LeetCode 中階衝刺（Weeks 5–8）

#### Week 5：SQL 實戰、PostgreSQL 整合與雙指針/滑動視窗（18h）
- **Backend (7.5h)**:
  - Day 1-2: PostgreSQL 安裝與存取、建立 Users/Projects/Tasks 資料表 Schema (2.5h)
  - Day 3-4: 手寫 SQL SELECT/INSERT/UPDATE/DELETE 與 JOIN 語法練習 (2.5h)
  - Day 5: 建立 PostgreSQL pytest Integration Test 環境 (2.5h)
- **Agent (3.75h)**:
  - Day 1-3: Prompt Versioning 機制與記錄每次 Agent Run 的 Raw IO (2h)
  - Day 4-5: 建立 Agent 運行日誌持久化模組 (1.75h)
- **LeetCode (3.75h - 滑動視窗與 Stack)**:
  - Day 1-2: LC 3. Longest Substring Without Repeating Characters (Medium)
  - Day 3-4: LC 424. Longest Repeating Character Replacement (Medium)
  - Day 5: LC 20. Valid Parentheses (Easy) & LC 155. Min Stack (Medium)
- **緩衝 (3h)**: 雙週進度除錯與 LeetCode 檢討

#### Week 6：SQLAlchemy ORM、Alembic Migration 與二分搜尋/鏈結串列（18h）
- **Backend (7.5h)**:
  - Day 1-2: SQLAlchemy ORM Models 定義與 Repository 層改寫 (3h)
  - Day 3-4: Alembic Migration 初始化、Generate & Upgrade 實戰 (2.5h)
  - Day 5: Repository 層與資料庫的事務 (Transaction Rollback) 測試 (2h)
- **Agent (3.75h)**:
  - Day 1-3: Semantic Validator 語意檢查模組實作 (2h)
  - Day 4-5: 針對 Validation Failures 產生精準修復 Prompt (1.75h)
- **LeetCode (3.75h - Binary Search & Linked List)**:
  - Day 1-2: LC 704. Binary Search (Easy) & LC 74. Search a 2D Matrix (Medium)
  - Day 3-4: LC 875. Koko Eating Bananas (Medium)
  - Day 5: LC 206. Reverse Linked List (Easy) & LC 141. Linked List Cycle (Easy)
- **緩衝 (3h)**: 進度補齊與演算法複習

#### Week 7：資料庫優化與圖論/循環依賴（18h）
- **Backend (7.5h)**:
  - Day 1-2: PostgreSQL Pagination (Limit/Offset) & Filtering & Sorting 實作 (3h)
  - Day 3-4: Index (單欄/複合索引) 原理與 EXPLAIN 查詢計畫優化 (2.5h)
  - Day 5: 完成完整 Task Service 的 DB 整合測試 suite (2h)
- **Agent (3.75h - ✅ Ex-07 已提前完成，本週進行優化與測試重構)**:
  - Day 1-3: DAG 有向無環圖依賴圖建立與 DFS 循環依賴檢測 (已完成)
  - Day 4-5: 擴充 TaskPlan 依賴衝突分析與極端情境單元測試 (1.75h)
- **LeetCode (3.75h - Binary Tree & DFS/BFS)**:
  - Day 1-2: LC 226. Invert Binary Tree (Easy) & LC 104. Maximum Depth of Binary Tree (Easy)
  - Day 3-4: LC 102. Binary Tree Level Order Traversal (Medium)
  - Day 5: LC 235. Lowest Common Ancestor of a BST (Medium)
- **緩衝 (3h)**: 樹狀結構與圖論演算法總結

#### Week 8：Month 2 整合、系統日誌與圖論進階（18h）
- **Backend (7.5h)**:
  - Day 1-2: Environment Variables (.env) 設定解耦 (AppConfig) (2.5h)
  - Day 3-4: Request ID 中間件 (Middleware) 與 Structured JSON Logging (2.5h)
  - Day 5: API 全流程 Integration Test 驗收 (2.5h)
- **Agent (3.75h)**:
  - Day 1-3: 整合 Generate → Validate → Feedback → Retry 全流程 Agent Loop (2h)
  - Day 4-5: 執行 20 個 Benchmark 案例並輸出 Failure Analysis (1.75h)
- **LeetCode (3.75h - Graph & Topological Sort - 台積電高頻)**:
  - Day 1-2: LC 200. Number of Islands (Medium)
  - Day 3-4: LC 207. Course Schedule (Medium - 拓撲排序，與 Agent 依賴相同原理)
  - Day 5: LC 210. Course Schedule II (Medium)
- **緩衝 (3h)**: Month 2 Gate 技術驗收與演算法測驗

---

### 🟠 Month 3：Docker、CI/CD、系統設計與模擬面試（Weeks 9–12）

#### Week 9：Docker 容器化與 Heap / Priority Queue（18h）
- **Backend (7.5h)**:
  - Day 1-2: FastAPI 多階段編譯 Dockerfile 撰寫 (2.5h)
  - Day 3-4: Docker Compose 整合 API 與 PostgreSQL 服務 (2.5h)
  - Day 5: 在 Docker 容器環境中自動執行 pytest 測試 (2.5h)
- **Agent (3.75h)**:
  - Day 1-3: Structured Metric Collector (記錄 Latency, Token Cost, Retry Times) (2h)
  - Day 4-5: 產出 Evaluation JSON 報告檔 (1.75h)
- **LeetCode (3.75h - Heap & Priority Queue)**:
  - Day 1-2: LC 703. Kth Largest Element in a Stream (Easy)
  - Day 3-4: LC 215. Kth Largest Element in an Array (Medium)
  - Day 5: LC 973. K Closest Points to Origin (Medium)
- **緩衝 (3h)**: Docker Compose 與容器網路排錯

#### Week 10：GitHub Actions CI/CD 與 動態規劃 DP（18h）
- **Backend (7.5h)**:
  - Day 1-2: GitHub Actions Workflow 設定 (.github/workflows/ci.yml) (3h)
  - Day 3-4: 自動化拉取 PostgreSQL Service 執行整合測試 (2.5h)
  - Day 5: Code Formatting (Ruff/Black) 與 Type Check (mypy) 檢查點設定 (2h)
- **Agent (3.75h)**:
  - Day 1-3: Agent 評估指標分析 (Schema Pass Rate, First-attempt Pass Rate, Latency vs Cost) (2h)
  - Day 4-5: 完成完整 Evaluation Report Markdown (1.75h)
- **LeetCode (3.75h - Dynamic Programming 基礎)**:
  - Day 1-2: LC 70. Climbing Stairs (Easy) & LC 746. Min Cost Climbing Stairs (Easy)
  - Day 3-4: LC 198. House Robber (Medium)
  - Day 5: LC 213. House Robber II (Medium)
- **緩衝 (3h)**: CI 流程偵錯與 DP 轉移方程式練習

#### Week 11：作品集整合、系統設計基礎與 DP 進階（18h）
- **Backend (7.5h)**:
  - Day 1-2: 完善 Backend API 專案 README.md (架構圖、快速啟動指令、curl 範例) (3h)
  - Day 3-4: 台積電 IT 常考系統設計基礎：Load Balancer, Caching (Redis 原理), Connection Pool (2.5h)
  - Day 5: 準備 5 分鐘後端架構說明簡報/講稿 (2h)
- **Agent (3.75h)**:
  - Day 1-3: 擴充 Agent Benchmark 至 30 個測試情境 (2h)
  - Day 4-5: 錄製/撰寫 3 分鐘 Agent Workflow 實機演示與限制說明 (1.75h)
- **LeetCode (3.75h - DP 進階與台積電高頻模擬)**:
  - Day 1-2: LC 322. Coin Change (Medium)
  - Day 3-4: LC 300. Longest Increasing Subsequence (Medium)
  - Day 5: LC 1143. Longest Common Subsequence (Medium)
- **緩衝 (3h)**: 系統設計問答準備與模擬測驗

#### Week 12：台積電 IT 模擬面試、OA 總複習與最終驗收（18h）
- **Backend (7.5h)**:
  - Day 1-2: 無 AI 從零建立小型帶 DB 驗證之 API (3h)
  - Day 3-4: 模擬後端與資料庫技術問答 (SQL, Index, Transaction, FastAPI, Async) (2.5h)
  - Day 5: 履歷精修與專案 Highlights 提煉 (2h)
- **Agent (3.75h)**:
  - Day 1-3: 模擬 AI/Agent Engineer 技術面試問答 (Structured Output, Validation, Retry, Evaluation) (2h)
  - Day 4-5: 整理 Agent 限制與未來改進方向 (1.75h)
- **LeetCode (3.75h - 台積電 IT 模擬 HackerRank OA 測驗)**:
  - Day 1-2: 模擬測驗 1 (60 分鐘內完成 1 Easy + 1 Medium)
  - Day 3-4: 模擬測驗 2 (90 分鐘內完成 2 Medium)
  - Day 5: 高頻錯題與演算法模板最後總複習
- **緩衝 (3h)**: 全套模擬面試演練 (Behavioral + Technical + OA)

---

### 🔴 Days 85–90：最終緩衝與面試衝刺（Final Buffer）

- 專注處理：
  1. LeetCode 高頻題型錯題複習。
  2. GitHub Repositories 整理與 README 優化。
  3. 台積電 IT 履歷投遞與自我介紹演練。
  4. 絕對不新增任何新功能。

---

## 4) 每週與每月檢查機制 (Definition of Done)

### 每日檢查點 (Daily DoD)
- 當天演算法題需通過所有測項，並於筆記記錄時間/空間複雜度。
- 當天 API / Agent 程式碼需寫好單元測試且 `pytest` 100% 通過。

### 每週檢查點 (Weekly DoD)
- **週五/週六檢討**：核對本週 3 大軌道進度完成度。
- **時數控管**：確認未超過 18 小時上限；若落後則使用 3 小時緩衝時間，或依規定刪減 Optional 題目。

### 每月 Gate 驗收標準 (Monthly Gate)
- **Month 1 Gate (✅ 通過)**：無 AI 獨立寫出三層架構 REST API，測試覆蓋完整；Agent 基礎 Retry 通過。
- **Month 2 Gate**：PostgreSQL Migration 與 CRUD 正常運作；Agent DAG 循環依賴檢測 100% 正確；LeetCode 累積完成 20+ 題 Medium。
- **Month 3 Gate**：Docker Compose 與 GitHub Actions CI 綠燈；Agent Evaluation 報告產出；LeetCode 累積 45+ 題，模擬 HackerRank 測驗能穩定通過。
