"""V26 最小入口：确认 SQLite 里有 Account 数据。

开发启动：
uv run fastapi dev lessons/v26/app/main.py --port 8001
"""

from fastapi import FastAPI

from .database import init_db
from .routers import accounts

app = FastAPI(title="python_learn v26", version="0.1.0")
app.include_router(accounts.router)
init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v26 isolation", "hint": "uv run python lessons/v26/seed.py"}
