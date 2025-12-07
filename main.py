import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from app.core.config import settings
from app.models.models import Base
from app.database.db import engine
from app.api.router import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format=settings.LOG_FORMAT,
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: create tables if not exist (for simple deployments)
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.include_router(api_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

# 添加统一的异常处理器
@app.exception_handler(Exception)
async def catch_all_exceptions(request, exc):
    # 打印异常信息
    logger.warning(f"Exception caught for request {request.url}: {exc}", exc_info=True)
    if isinstance(exc, ExceptionGroup):
        message = str(exc.exceptions[0])
    else:
        message = exc
    # 返回自定义的错误信息和 HTTP 状态码
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"code": 500, "msg": f"服务发生异常, {message}"})


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
