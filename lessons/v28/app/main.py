"""V28 入口：真实 MySQL + AsyncEngine / AsyncSession。

开发启动：
uv run fastapi dev lessons/v28/app/main.py --port 8001
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import engine, init_schema
from .routers import health, orders, users


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    await init_schema()
    yield
    await engine.dispose()


app = FastAPI(title="python_learn v28", version="0.1.0", lifespan=lifespan)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(orders.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "v28 async mysql", "hint": "copy lessons/v28/.env.example to lessons/v28/.env"}
