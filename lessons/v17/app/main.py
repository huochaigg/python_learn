"""V17 入口：只创建 FastAPI() 并注册 Router。

学习目标：
1. main 负责组装，接口写在 APIRouter 里。
2. Request Schema 和 Response Schema 分开。
3. response_model 会过滤、校验、序列化响应。

开发启动（项目根目录）：
uv run fastapi dev lessons/v17/app/main.py --port 8001

等价理解用：
uv run uvicorn lessons.v17.app.main:app --reload --port 8001
"""

from fastapi import FastAPI

from lessons.v17.app.routers import orders, users

app = FastAPI(title="python_learn v17", version="0.1.0")

# include_router(router)：接收一个 APIRouter，把它里面已经注册的 Path Operation
# 合并进当前 FastAPI App。这是应用启动阶段的路由注册，不是发 HTTP 请求。
# NestJS 对照：有点像在 Module 里把 Controller 登记到应用上，底层实现不同。
app.include_router(users.router)
app.include_router(orders.router)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "v17 routers + response model"}


# 本文件重点：
# 1. main.py 不要继续堆业务接口。
# 2. include_router 只做注册；prefix/tags 写在各自 APIRouter 上。
# 3. users / orders 两套 Router、两套 Schema 独立存在。
