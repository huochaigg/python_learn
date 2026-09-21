"""V25 入口：约束 / IntegrityError / 幂等。

开发启动：
uv run fastapi dev lessons/v25/app/main.py --port 8001
"""

from fastapi import FastAPI

from lessons.v25.app.database import init_db
from lessons.v25.app.handlers import register_exception_handlers
from lessons.v25.app.routers import orders, users

app = FastAPI(title="python_learn v25", version="0.1.0")
register_exception_handlers(app)
app.include_router(users.router)
app.include_router(orders.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v25 constraints + idempotency"}
