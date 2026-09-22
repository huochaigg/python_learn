"""V27 入口：真实 MySQL + Engine/Pool + Settings。

开发启动：
uv run fastapi dev lessons/v27/app/main.py --port 8001
"""

from fastapi import FastAPI

from .database import init_schema
from .routers import health, users

app = FastAPI(title="python_learn v27", version="0.1.0")
app.include_router(health.router)
app.include_router(users.router)
init_schema()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v27 mysql + pool", "hint": "copy lessons/v27/.env.example to lessons/v27/.env"}
