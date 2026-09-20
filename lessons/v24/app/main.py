"""V24 入口：并发库存（lost update / FOR UPDATE / version / atomic UPDATE）。

开发启动：
uv run fastapi dev lessons/v24/app/main.py --port 8001

先 seed：
uv run python -m lessons.v24.seed
"""

from fastapi import FastAPI

from lessons.v24.app.database import init_db
from lessons.v24.app.handlers import register_exception_handlers
from lessons.v24.app.routers import orders, stocks

app = FastAPI(title="python_learn v24", version="0.1.0")
register_exception_handlers(app)
app.include_router(stocks.router)
app.include_router(orders.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v24 concurrency", "hint": "uv run python -m lessons.v24.seed"}
