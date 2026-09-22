"""V29 入口：OpenAI Agents SDK + FastAPI + AsyncSession。

开发启动：
uv run fastapi dev lessons/v29/app/main.py --port 8001
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .core.database import engine, init_schema, seed_products
from .routers.agent_router import router as agent_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_schema()
    await seed_products()
    yield
    await engine.dispose()


app = FastAPI(title="python_learn v29", version="0.1.0", lifespan=lifespan)
app.include_router(agent_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
