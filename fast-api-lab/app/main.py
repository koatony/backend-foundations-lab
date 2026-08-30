from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from app.schemas.error import ErrorResponse
from app.exceptions.exceptions import ItemNotFoundError, DuplicateItemError
from app.routers.items import router as items_router
from app.core import settings
from app.routers.tasks import router as tasks_router
from app.exceptions.exceptions import TaskNotFoundError

from app.middleware.logging import CorrelationIDMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0"
)
# 註冊中間件
app.add_middleware(CorrelationIDMiddleware)


app.include_router(items_router)
app.include_router(tasks_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    error_data = ErrorResponse(
        code=f"HTTP_{exc.status_code}",
        message=exc.detail,
        detail={"path": request.url.path}
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_data.model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    error_data = ErrorResponse(
        code=f"HTTP_{status.HTTP_422_UNPROCESSABLE_ENTITY}",
        message="Invalid request body",
        detail={
            "path": request.url.path,
            "errors": jsonable_encoder(exc.errors())
        }
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_data.model_dump()
    )


@app.exception_handler(ItemNotFoundError)
async def itemnotfound_exception_handler(
    request: Request,
    exc: ItemNotFoundError
) -> JSONResponse:
    error_data = ErrorResponse(
        code="NOT_FOUND",
        message=str(exc),
        detail={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_data.model_dump()
    )


@app.exception_handler(DuplicateItemError)
async def duplicateitem_exception_handler(
    request: Request,
    exc: DuplicateItemError
) -> JSONResponse:
    error_data = ErrorResponse(
        code="DUPLICATE_ITEM",
        message=str(exc),
        detail={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_data.model_dump()
    )


# task exception
@app.exception_handler(TaskNotFoundError)
async def tasknotfound_exception_handler(
    request: Request,
    exc: TaskNotFoundError
) -> JSONResponse:
    error_data = ErrorResponse(
        code="NOT_FOUND",
        message=str(exc),
        detail={"path": request.url.path}
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error_data.model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    error_data = ErrorResponse(
        code = "INTERNAL_SERVER_ERROR",
        message = "Internal Server Error",
        detail = {"path": request.url.path, "exception": str(exc)}
    )
    
    return JSONResponse(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        content = error_data.model_dump()
    )
    