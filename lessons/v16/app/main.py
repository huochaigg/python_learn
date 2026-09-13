"""V16 FastAPI 入门：把 HTTP 请求映射到 Python 函数。

学习目标：
1. FastAPI 如何根据函数签名区分 Path / Query / Body。
2. Pydantic BaseModel 会做运行时校验，和普通 annotation 不同。
3. 会看 Swagger /docs，并故意提交错误数据。

开发启动（项目根目录）：
uv run fastapi dev lessons/v16/app/main.py

等价理解用：
uv run uvicorn lessons.v16.app.main:app --reload
"""

from typing import Annotated, Any

from fastapi import FastAPI, HTTPException, Path, Query

from lessons.v16.app.models import UserCreate, UserUpdate

# FastAPI：ASGI Web 框架的应用类，建立在 Starlette + Pydantic 之上。
# 调用 FastAPI() 得到 app 实例，之后用 @app.get / @app.post 往这个实例上注册路由。
# NestJS 粗对照：有点像创建应用后再注册 Controller，但模块系统和 DI 机制并不一样。
app = FastAPI(title="python_learn v16", version="0.1.0")

# 内存存储：只为了让 CRUD 能看见结果。V16 不拆 Repository/Service，也不接数据库。
_users: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Ada",
        "age": 30,
        "email": "ada@example.com",
        "active": True,
    }
}
_next_id = 2


def plain_python_echo(age: int) -> dict[str, str]:
    """普通 Python 函数：age: int 默认不会在运行时拦住错误类型。"""
    return {"got": str(age), "python_type": type(age).__name__}


@app.get("/")
def root() -> dict[str, str]:
    # @app.get(path)：Path Operation Decorator（V11 decorator）。
    # 作用：把 HTTP GET + 这个 path，绑定到下面的 Python 函数。
    # NestJS 对照：@Get("/")，底层实现不同，不要当成同一个 decorator。
    return {"message": "v16 fastapi"}


@app.get("/health")
async def health() -> dict[str, bool]:
    # FastAPI 同时支持 def 和 async def。
    # 有 await（异步 DB / HTTP）再用 async def；不要看见框架就全部机械改成 async。
    return {"ok": True}


@app.get("/demo/plain-vs-fastapi")
def plain_vs_fastapi() -> dict[str, object]:
    # 对比：普通函数即使标注 int，传入 str 也能进来。
    # FastAPI/Pydantic 会读取 annotation，对 HTTP 请求做解析和 validation。
    echoed = plain_python_echo("not-an-int")  # type: ignore[arg-type]
    return {
        "plain_function_received": echoed,
        "try_next": "GET /users/abc 会被 FastAPI 校验拦住，返回 422",
    }


@app.get("/users")
def list_users(
    page: int = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="每页条数")] = 20,
    keyword: Annotated[str | None, Query(max_length=50, description="按名字过滤")] = None,
) -> dict[str, object]:
    # Query 参数：不在 URL path 里的简单类型，FastAPI 通常当成 query string。
    # 例如 GET /users?page=1&limit=20&keyword=Ada
    # NestJS 对照：@Query("page") page: number，FastAPI 多数时候靠参数名+类型推断。
    #
    # Annotated[int, Query(...)]：真实类型仍是 int；Query(...) 是给 FastAPI 的 metadata。
    # FastAPI 读取 Annotated 里的 Query，做校验、默认值和 OpenAPI 文档。
    # 不是所有参数都要 Annotated：page 这种简单默认值保持普通写法即可。
    #
    # keyword: str | None = None
    # - str | None：值允许是 None（V10）
    # - = None：可以不传，这时才是「查询参数可省略」
    # 只有 str | None 没有默认值，通常仍然 required。
    start = (page - 1) * limit
    items = list(_users.values())
    if keyword:
        items = [row for row in items if keyword.lower() in str(row["name"]).lower()]
    return {"page": page, "limit": limit, "items": items[start : start + limit]}


@app.get("/users/{user_id}")
def get_user(
    user_id: Annotated[int, Path(ge=1, description="用户 ID，必须 >= 1")],
) -> dict[str, Any]:
    # Path 参数：路由里写了 {user_id}，函数里同名参数，FastAPI 就从 URL 路径取值。
    # /users/123 -> user_id=123（int）；/users/abc 无法转 int，自动 422。
    # Path()：专门给路径参数加校验/文档；Query() 则是查询字符串。
    # 访问 /users/0 会因为 ge=1 失败。
    user = _users.get(user_id)
    if user is None:
        # HTTPException：本课只用来返回 404。不是自定义 exception handler，后面版本再展开。
        raise HTTPException(status_code=404, detail=f"user not found: {user_id}")
    return user


@app.post("/users")
def create_user(user: UserCreate) -> dict[str, Any]:
    # @app.post：HTTP POST 的 Path Operation。NestJS 对照 @Post()。
    # 参数类型是 BaseModel 子类 -> FastAPI 当成 JSON Request Body，不是 Query。
    global _next_id
    # model_dump()：Pydantic V2 把模型转成普通 dict。
    # 旧教程常见 .dict()；当前项目和官方示例优先 model_dump()。
    payload = user.model_dump()
    saved = {"id": _next_id, **payload}
    _users[_next_id] = saved
    _next_id += 1
    return saved


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: UserUpdate,
    notify: bool = False,
) -> dict[str, Any]:
    # 同一函数里 FastAPI 按签名区分来源：
    # 1. 名字出现在 path 的 {user_id} 里 -> Path
    # 2. 类型是 Pydantic BaseModel -> Body
    # 3. 其余简单类型（bool/int/str）-> Query，例如 ?notify=true
    # NestJS 往往要同时写 @Param @Body @Query；FastAPI 先靠声明推断。
    current = _users.get(user_id)
    if current is None:
        raise HTTPException(status_code=404, detail=f"user not found: {user_id}")
    patch = user.model_dump(exclude_unset=True)
    current.update(patch)
    return {"user": current, "notify": notify}


@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> dict[str, Any]:
    # @app.delete：HTTP DELETE。演示用，不做复杂级联删除。
    user = _users.pop(user_id, None)
    if user is None:
        raise HTTPException(status_code=404, detail=f"user not found: {user_id}")
    return {"deleted": user}


# 本文件重点：
# 1. FastAPI 读函数签名：Path 对占位符，简单类型常是 Query，BaseModel 常是 Body。
# 2. 普通 Python annotation 默认不校验；FastAPI/Pydantic 会拿去解析请求。
# 3. str | None 和 = None 是两件事。
# 4. 开发看 /docs；故意传错类型，观察 422 validation error。
