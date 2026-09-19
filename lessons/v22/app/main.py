"""V22 入口：订单一对多 Relationship。

开发启动：
uv run fastapi dev lessons/v22/app/main.py --port 8001

先 seed：
uv run python -m lessons.v22.seed
"""

from fastapi import FastAPI

from lessons.v22.app.database import init_db
from lessons.v22.app.handlers import register_exception_handlers
from lessons.v22.app.routers import orders

app = FastAPI(title="python_learn v22", version="0.1.0")
register_exception_handlers(app)
app.include_router(orders.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v22 sqlalchemy relationship", "hint": "uv run python -m lessons.v22.seed"}
