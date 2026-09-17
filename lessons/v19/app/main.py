"""V19 入口：注册 exception handler 和 Router。

学习目标：
1. Service raise 业务异常，不要直接 HTTPException。
2. exception_handler 把异常转成统一 JSON + 正确 HTTP status。
3. 校验失败是 422；未知错误是 500 且不泄露 traceback。

开发启动（项目根目录）：
uv run fastapi dev lessons/v19/app/main.py --port 8001

等价理解用：
uv run uvicorn lessons.v19.app.main:app --reload --port 8001
"""

from fastapi import FastAPI

from lessons.v19.app.handlers.exception_handlers import register_exception_handlers
from lessons.v19.app.routers import demo, orders, users

app = FastAPI(title="python_learn v19", version="0.1.0")

# 先注册 handler，再挂 Router。handler 是启动时的「异常 → Response」规则，不是发请求。
register_exception_handlers(app)

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(demo.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v19 exceptions"}


# 本文件重点：
# 1. main 组装：handler + router。
# 2. Router 保持薄，不要到处 try/except BizException。
# 3. Service 描述业务失败；Handler 负责 HTTP。
