"""V20 入口：create_all + 注册 Session 依赖的 users Router。

学习目标：
1. Engine / sessionmaker / Session 各是什么。
2. Mapped + mapped_column 声明表。
3. add / commit / select / get / delete 这条 CRUD 链。

开发启动（项目根目录）：
uv run fastapi dev lessons/v20/app/main.py --port 8001
"""

from fastapi import FastAPI

from lessons.v20.app.database import init_db
from lessons.v20.app.handlers import register_exception_handlers
from lessons.v20.app.routers import users

app = FastAPI(title="python_learn v20", version="0.1.0")
register_exception_handlers(app)
app.include_router(users.router)

# create_all 前 User 必须已被 import（database.init_db 里会 import）。
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v20 sqlalchemy sqlite"}
