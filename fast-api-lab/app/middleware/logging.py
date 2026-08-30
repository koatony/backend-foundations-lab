import uuid
import time
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response



# 宣告ContextVar 
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id",default="")


def get_correlation_id() -> str:
     """提供給系統任何地方（如 Logger、Service）取得當前 Request Trace ID 的工具函式"""
     return correlation_id_ctx.get()


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # A. 洋蔥圈入口：檢查 Header，若客戶端沒帶則自動生成 UUID
        cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        
        # B. 設定到當前 async task 的 ContextVar 中
        token = correlation_id_ctx.set(cid)
        start_time = time.perf_counter()

        try:
            # C. 呼叫洋蔥圈內層（進入你的 Router、Service、Repository）
            response = await call_next(request)

        finally:
                process_time = time.perf_counter() - start_time

        
        # D. 洋蔥圈出口：在 Response Header 帶回 Trace ID 與執行總耗時
        response.headers["X-Correlation-ID"] = cid
        response.headers["X-Process-Time"] = f"{process_time:.4f}s"

        # E. 清理上下文標籤 (Reset Token)
        correlation_id_ctx.reset(token)
        return response
    


# 
