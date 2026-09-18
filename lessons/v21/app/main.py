"""V21 入口：单表列表查询（筛选 / 排序 / 分页 / count）。

开发启动：
uv run fastapi dev lessons/v21/app/main.py --port 8001

先 seed：
uv run python -m lessons.v21.seed
"""

from fastapi import FastAPI

from lessons.v21.app.database import init_db
from lessons.v21.app.handlers import register_exception_handlers
from lessons.v21.app.routers import users

app = FastAPI(title="python_learn v21", version="0.1.0")
register_exception_handlers(app)
app.include_router(users.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v21 sqlalchemy query", "hint": "uv run python -m lessons.v21.seed"}
