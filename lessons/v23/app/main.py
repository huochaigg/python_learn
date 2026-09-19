"""V23 入口：事务（commit / rollback / flush / begin）。

开发启动：
uv run fastapi dev lessons/v23/app/main.py --port 8001

先 seed：
uv run python -m lessons.v23.seed
"""

from fastapi import FastAPI

from lessons.v23.app.database import init_db
from lessons.v23.app.handlers import register_exception_handlers
from lessons.v23.app.routers import orders, stocks

app = FastAPI(title="python_learn v23", version="0.1.0")
register_exception_handlers(app)
app.include_router(stocks.router)
app.include_router(orders.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v23 sqlalchemy transaction", "hint": "uv run python -m lessons.v23.seed"}
