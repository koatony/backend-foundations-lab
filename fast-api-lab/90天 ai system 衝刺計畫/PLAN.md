<aside>
<img src="i" alt="i" width="40px" />

本計畫專為 **Backend Foundations & AI Agent Systems Engineering** 打造；聚焦高可用後端工程化能力與不依賴框架的 AI Agent 實務。

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

## 1) 職涯目標

### 目標職位
1. AI Systems Engineer / AI Agent Engineer
2. AI Backend Engineer / Python Backend Engineer
3. Production Systems Engineer

### 核心交付與檢驗能力
- 獨立撰寫高維護性 RESTful API (FastAPI + Pydantic + 三層 Clean Architecture)。
- PostgreSQL 資料庫設計、Migration (Alembic)、Indexing 與 Transaction 優化。
- 完整單元與整合測試 (pytest + Mock + Fixtures + AAA 規範)。
- Docker 容器化與 Multi-container 部署 (Docker Compose)。
- CI/CD 自動化流程 (GitHub Actions)。
- LLM Agent 結構化輸出 (Structured Output) 驗證與重試機制 (Generate-Validate-Retry)。
- 有向無環圖 (DAG) 任務依賴解析與循環依賴檢測。
- Agent 評估指標 (Latency, Cost, Accuracy Benchmark)。

---

## 2) 雙主線專案與交付物（Deliverables）

### Track A：backend-foundations-lab (Task Management REST API)
- **核心架構**：FastAPI + Pydantic + PostgreSQL + SQLAlchemy + Alembic + Docker + GitHub Actions
- **交付物**：Production-ready RESTful API、完整 API 測試 suite (Coverage > 85%)、Docker Compose 配置檔。

### Track B：agent-workflow-lab (AI TaskPlan Agent)
- **核心架構**：Gemini / OpenRouter API + Pydantic Schema + DFS 循環依賴檢測 + Structured Feedback Retry Loop
- **交付物**：不依賴框架的自研 Agent Loop、Benchmark 測試集 (30+ 測試案例)、評估報告 (Evaluation Report)。

---

## 3) 90 天週次規劃表 (Backend & Agent Focused)

### 🟢 Month 1：後端基礎與 Agent 核心（Weeks 1–4）

> **【當前狀態】後端與 Agent 軌道已 100% 完成 (Ex-01 ~ Ex-06，25 個測試全過)。**

- **Backend (✅ 已完成)**: Python 基礎、Context Manager、Exception Bubbling、JSON Validator、Task REST API v0.1 (三層架構)。
- **Agent (✅ 已完成)**: TaskPlan Schema、Gemini Tool Parser、Generate-Validate-Retry Agent Loop。

---

### 🟡 Month 2：PostgreSQL 資料庫與 Agent 高級驗證（Weeks 5–8）

#### Week 5：SQL 實戰與 PostgreSQL 整合（18h）
- **Backend (9.0h)**:
  - Day 1-2: PostgreSQL 安裝與存取、建立 Users/Projects/Tasks 資料表 Schema (4h)
  - Day 3-4: 手寫 SQL SELECT/INSERT/UPDATE/DELETE 與 JOIN 語法練習 (3h)
  - Day 5: 建立 PostgreSQL pytest Integration Test 環境 (2h)
- **Agent (6.0h)**:
  - Day 1-3: Prompt Versioning 機制與記錄每次 Agent Run 的 Raw IO (3.5h)
  - Day 4-5: 建立 Agent 運行日誌持久化模組 (2.5h)
- **緩衝 (3.0h)**: 進度除錯與重構

#### Week 6：SQLAlchemy ORM 與 Alembic Migration（18h）
- **Backend (9.0h)**:
  - Day 1-2: SQLAlchemy ORM Models 定義與 Repository 層改寫 (4h)
  - Day 3-4: Alembic Migration 初始化、Generate & Upgrade 實戰 (3h)
  - Day 5: Repository 層與資料庫的事務 (Transaction Rollback) 測試 (2h)
- **Agent (6.0h)**:
  - Day 1-3: Semantic Validator 語意檢查模組實作 (3.5h)
  - Day 4-5: 針對 Validation Failures 產生精準修復 Prompt (2.5h)
- **緩衝 (3.0h)**: 進度補齊與單元測試

#### Week 7：資料庫優化與圖論依賴驗證（18h）
- **Backend (9.0h)**:
  - Day 1-2: PostgreSQL Pagination (Limit/Offset) & Filtering & Sorting 實作 (4h)
  - Day 3-4: Index (單欄/複合索引) 原理與 EXPLAIN 查詢計畫優化 (3h)
  - Day 5: 完成完整 Task Service 的 DB 整合測試 suite (2h)
- **Agent (6.0h - ✅ Ex-07 已提前完成，本週進行優化與測試重構)**:
  - Day 1-3: DAG 有向無環圖依賴圖建立與 DFS 循環依賴檢測 (已完成)
  - Day 4-5: 擴充 TaskPlan 依賴衝突分析與極端情境單元測試 (2.5h)
- **緩衝 (3.0h)**: 雙週技術總結

#### Week 8：Month 2 整合、系統日誌與 Agent 評估（18h）
- **Backend (9.0h)**:
  - Day 1-2: Environment Variables (.env) 設定解耦 (AppConfig) (3h)
  - Day 3-4: Request ID 中間件 (Middleware) 與 Structured JSON Logging (3h)
  - Day 5: API 全流程 Integration Test 驗收 (3h)
- **Agent (6.0h)**:
  - Day 1-3: 整合 Generate → Validate → Feedback → Retry 全流程 Agent Loop (3.5h)
  - Day 4-5: 執行 20 個 Benchmark 案例並輸出 Failure Analysis (2.5h)
- **緩衝 (3.0h)**: Month 2 Gate 技術驗收

---

### 🟠 Month 3：Docker、CI/CD、系統設計與面試準備（Weeks 9–12）

#### Week 9：Docker 容器化與服務整合（18h）
- **Backend (9.0h)**:
  - Day 1-2: FastAPI 多階段編譯 Dockerfile 撰寫 (3.5h)
  - Day 3-4: Docker Compose 整合 API 與 PostgreSQL 服務 (3.5h)
  - Day 5: 在 Docker 容器環境中自動執行 pytest 測試 (2h)
- **Agent (6.0h)**:
  - Day 1-3: Structured Metric Collector (記錄 Latency, Token Cost, Retry Times) (3.5h)
  - Day 4-5: 產出 Evaluation JSON 報告檔 (2.5h)
- **緩衝 (3.0h)**: Docker Compose 與容器網路排錯

#### Week 10：GitHub Actions CI/CD 自動化（18h）
- **Backend (9.0h)**:
  - Day 1-2: GitHub Actions Workflow 設定 (.github/workflows/ci.yml) (4h)
  - Day 3-4: 自動化拉取 PostgreSQL Service 執行整合測試 (3h)
  - Day 5: Code Formatting (Ruff/Black) 與 Type Check (mypy) 檢查點設定 (2h)
- **Agent (6.0h)**:
  - Day 1-3: Agent 評估指標分析 (Schema Pass Rate, First-attempt Pass Rate, Latency vs Cost) (3.5h)
  - Day 4-5: 完成完整 Evaluation Report Markdown (2.5h)
- **緩衝 (3.0h)**: CI 流程偵錯

#### Week 11：作品集整合與系統設計（18h）
- **Backend (9.0h)**:
  - Day 1-2: 完善 Backend API 專案 README.md (架構圖、快速啟動指令、curl 範例) (3.5h)
  - Day 3-4: 後端系統設計基礎：Load Balancer, Caching (Redis 原理), Connection Pool (3.5h)
  - Day 5: 準備 5 分鐘後端架構說明簡報/講稿 (2h)
- **Agent (6.0h)**:
  - Day 1-3: 擴充 Agent Benchmark 至 30 個測試情境 (3.5h)
  - Day 4-5: 錄製/撰寫 3 分鐘 Agent Workflow 實機演示與限制說明 (2.5h)
- **緩衝 (3.0h)**: 系統設計問答準備

#### Week 12：技術面試演練與最終驗收（18h）
- **Backend (9.0h)**:
  - Day 1-2: 無 AI 從零建立小型帶 DB 驗證之 API (4h)
  - Day 3-4: 模擬後端與資料庫技術問答 (SQL, Index, Transaction, FastAPI, Async) (3.5h)
  - Day 5: 履歷精修與專案 Highlights 提煉 (1.5h)
- **Agent (6.0h)**:
  - Day 1-3: 模擬 AI/Agent Engineer 技術面試問答 (Structured Output, Validation, Retry, Evaluation) (3.5h)
  - Day 4-5: 整理 Agent 限制與未來改進方向 (2.5h)
- **緩衝 (3.0h)**: 全套模擬面試演練 (Behavioral + Technical)

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

### 每月 Gate 驗收標準 (Monthly Gate)
- **Month 1 Gate (✅ 通過)**：無 AI 獨立寫出三層架構 REST API，測試覆蓋完整；Agent 基礎 Retry 通過。
- **Month 2 Gate**：PostgreSQL Migration 與 CRUD 正常運作；Agent DAG 循環依賴檢測 100% 正確。
- **Month 3 Gate**：Docker Compose 與 GitHub Actions CI 綠燈；Agent Evaluation 報告產出。
