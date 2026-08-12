# FastAPI 同步 (Sync) 與非同步 (Async) 核心架構與併發機制筆記

---

## 📌 Q&A 常見問答區 (Sync vs Async)

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

## 💡 額外知識點與進階觀念 (Extra Knowledge)

### 1. 核心底層技術：Starlette 與 AnyIO
- FastAPI 底層依賴 **Starlette** 框架。
- 當你定義一個一般的 `def` 路由時，Starlette 內部使用的是 `anyio.to_thread.run_sync`（或 `starlette.concurrency.run_in_threadpool`）來將同步函式包裝成非同步 Future 物件，並交由 `concurrent.futures.ThreadPoolExecutor` 執行。

### 2. Python GIL (Global Interpreter Lock) 對 Thread Pool 的影響
- Python 存在 GIL 限制：**同一時間只允許一個 Thread 真正執行 Python bytecode**。
- **I/O 密集型**：Thread 在等待網路或硬碟時會自動釋放 GIL，因此 Thread Pool 在此情境效能極佳。
- **CPU 密集型**：多個 Thread 會劇烈爭奪 GIL，導致 CPU 頻繁切換 Context Switch 增加額外開銷。因此**極重度的 CPU 運算應改用 `ProcessPoolExecutor` 或 Celery 異步任務佇列**。

### 3. Thread Pool 耗盡 (Thread Exhaustion) 的現象
- FastAPI 預設的 Thread Pool 上限通常為 **40 個 Threads** (基於 AnyIO 預設設定)。
- 若有 50 個併發請求同時呼叫耗時 10 秒的同步 `def` 介面：
  - 前 40 個請求會佔滿 Thread Pool。
  - 後 10 個同步請求會在 Queue 中排隊等待。
  - **重要好處**：此時主幹道 (Event Loop) **依然活著**！第 51 個呼叫高併發 `async def` 的請求依然能以毫秒級速度獲取回應！

---

## 🎯 實戰選擇指南 (Decision Matrix)

```
這支 API 裡面的主要操作是什麼？
│
├── 1. 純非同步套件 (如 httpx, asyncpg, aiofiles)
│     👉 使用【async def】+【await】 (極致效能/高吞吐量)
│
├── 2. 傳統同步阻塞套件 (如 requests, psycopg2, pandas)
│     👉 使用一般的【def】 (安全移交 ThreadPool，保護主幹道)
│
└── 3. 高 CPU 運算 (如 PIL 圖像處理, 機器學推論)
      👉 使用一般的【def】 或【背景任務 (Celery / ProcessPool)】
```

---
---

# 🛡️ FastAPI 錯誤處理與全域異常處理器 (Global Exception Handler) 筆記

## 📌 核心概念：責任分離 (Separation of Concerns)

> **核心口訣**：「Router 只管快樂路徑（Happy Path），錯誤則集中交給全域異常處理器（Global Exception Handler）。」

### 傳統寫法 vs 全域異常處理器寫法比較

| 比較項目 | 傳統寫法（Router 內處理 Exception） | 全域異常處理器寫法（Global Exception Handler） |
| :--- | :--- | :--- |
| **Router 責任** | 包含業務邏輯、`try...except` 與 `HTTPException` | 乾淨簡潔，只呼叫 Service 並回傳資料（Happy Path） |
| **程式碼重複性** | 每個 Router / Endpoint 都要重複寫 `try...except` | 集中在一處（`main.py`），全域適用 |
| **架構耦合度** | Service 層若拋出 `HTTPException` 會與 Web 框架強耦合 | Service 層只拋出純 Python **Domain Exception**，獨立於 Web |
| **可測試性** | 測試 Service 時需要模擬 HTTP 相關物件 | Service 測試只需驗證純 Python Exception，乾淨簡單 |

---

## 🛠️ 全域異常處理器三部曲實作流程

### 步驟 1：定義純 Domain Exceptions (`app/exceptions.py`)
Service 層只拋出這些領域異常，完全不依賴 FastAPI 或 `HTTPException`：
```python
# app/exceptions.py

class ItemNotFoundError(Exception):
    """當商品不存在時拋出"""
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"找不到 ID 為 {item_id} 的商品")

class DuplicateItemError(Exception):
    """當商品名稱重複時拋出"""
    def __init__(self, title: str):
        self.title = title
        super().__init__(f"商品名稱 '{title}' 已存在")
```

### 步驟 2：Service 層與 Router 層保持乾淨（Happy Path Only）
**Service 層**：只負責業務邏輯，遇到異常直接 `raise` Domain Exception。
```python
# app/services/item_service.py

class ItemService:
    def get_item(self, item_id: str) -> ItemResponse:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise ItemNotFoundError(item_id) # 拋出純 Domain Exception
        return item
```

**Router 層**：只管呼叫 Service，無須寫 `try...except`：
```python
# app/routers/items.py

@router.get("/{item_id}")
def get_item(item_id: str, service: ItemService = Depends()):
    return service.get_item(item_id)  # 發生錯誤時自動向上冒泡 (Bubbling)
```

### 步驟 3：在 FastAPI 主程式註冊全域異常處理器 (`main.py`)
使用 `@app.exception_handler(ExceptionClass)` 攔截特定 Exception，轉化為格式統一的 `JSONResponse`：
```python
# app/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.exceptions import ItemNotFoundError, DuplicateItemError

app = FastAPI()

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "code": "ITEM_NOT_FOUND",
            "message": str(exc),
            "detail": {"path": request.url.path, "item_id": exc.item_id}
        }
    )

@app.exception_handler(DuplicateItemError)
async def duplicate_item_handler(request: Request, exc: DuplicateItemError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": "DUPLICATE_ITEM",
            "message": str(exc),
            "detail": {"path": request.url.path, "title": exc.title}
        }
    )
```

---

## 💡 常見問答區 (Q&A)

### Q1: 為什麼 Service 層不可以直接 `raise HTTPException(status_code=404, detail="...")`？
- **解答**：因為 `HTTPException` 是 FastAPI / Starlette 的 Web 框架元件。如果 Service 層出現 HTTP 觀念，當這套商業邏輯未來被移植到 CLI 命令行工具、Celery 背景任務、或者 WebSocket 服務時，就會強綁定 Web 框架，無法獨立運作與測試。

### Q2: 全域異常處理器與 Exception Bubbling（錯誤向上傳遞）的關係是什麼？
- **解答**：當 Service 層或 Repository 層拋出 Exception 時，因為 Router 層沒有寫 `try...except` 吞掉，Python 的機制會讓錯誤自動向外層呼叫堆疊傳遞 (Bubbling)，最終被最外層 FastAPI 的 `Global Exception Handler` 捕捉，實現優雅的錯誤攔截與轉換。
