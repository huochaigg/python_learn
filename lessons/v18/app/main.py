"""V18 入口：组装 Router。Depends Demo 写在 dependencies/ 和 routers/ 里。

学习目标：
1. Depends 传 callable，由 FastAPI 在请求阶段调用。
2. 依赖可以再依赖，形成树，而不是启动时平铺执行。
3. yield 适合 Session 的创建/清理；cache 只在同一次 Request 内。

开发启动（项目根目录）：
uv run fastapi dev lessons/v18/app/main.py --port 8001

等价理解用：
uv run uvicorn lessons.v18.app.main:app --reload --port 8001
"""

from fastapi import FastAPI

from lessons.v18.app.routers import demo, orders, users

app = FastAPI(title="python_learn v18", version="0.1.0")

app.include_router(users.router)
app.include_router(orders.router)
app.include_router(demo.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v18 Depends"}


# 本文件重点：
# 1. main 只注册 Router。
# 2. 可复用解析/鉴权/资源放 dependencies/，不要变成业务垃圾桶。
# 3. 教学接口集中在 /demo，users/orders 保持能看清复用。
