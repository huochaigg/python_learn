"""Agent 后端入口。长期演进项目，从 V32 起在本目录增量开发。

开发启动：
uv run fastapi dev projects/agent_backend/app/main.py --port 8001
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from .core.agent_exceptions import AgentRunError, error_payload
from .core.database import engine, init_schema, migrate_schema, seed_orders, seed_products
from .routers.agent_router import router as agent_router
from .routers.conversation_router import router as conversation_router
from .sessions.agent_session import init_sdk_session_tables

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await init_sdk_session_tables()
    yield
    await engine.dispose()


app = FastAPI(title="agent_backend", version="0.34.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(agent_router)
app.include_router(conversation_router)


@app.exception_handler(AgentRunError)
async def handle_agent_run_error(_request: Request, exc: AgentRunError) -> JSONResponse:
    # SDK Exception → Service map_sdk_exception → AgentRunError → 这里。
    # 不要把 str(exc.__cause__) 写进响应。
    return JSONResponse(status_code=exc.status_code, content=error_payload(exc))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
