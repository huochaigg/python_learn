"""V31 入口：Agents SDK Session + MySQL 会话历史。

开发启动：
uv run fastapi dev lessons/v31/app/main.py --port 8001
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .core.database import engine, init_schema, seed_products
from .routers.agent_router import router as agent_router
from .routers.conversation_router import router as conversation_router
from .sessions.agent_session import init_sdk_session_tables

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_schema()
    await seed_products()
    await init_sdk_session_tables()
    yield
    await engine.dispose()


app = FastAPI(title="python_learn v31", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(agent_router)
app.include_router(conversation_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(FRONTEND_DIR / "index.html")
