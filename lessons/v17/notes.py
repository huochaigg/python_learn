"""V17 速查：APIRouter + Response Model。

运行：uv run python lessons/v17/notes.py
"""

NOTES = """
APIRouter
  按业务域拆接口。router = APIRouter(prefix="/users", tags=["users"])
  NestJS 概念上接近 @Controller("users")，不是实现等价。

include_router
  启动时把 Router 上的 Path Operation 合并进 FastAPI App。
  不是发请求。main.py 只组装，不堆 CRUD。

prefix
  自动拼到该 Router 每条 path 前面。
  prefix="/users" + @router.get("") => GET /users

tags
  主要用于 OpenAPI/Swagger 分组，文档里 users / orders 分开。

Request Schema vs Response Schema
  UserCreate 收 password；UserResponse 没有 password。
  不要用同一份模型既当输入又当输出。

response_model
  不只是 Swagger：响应校验、序列化、按模型字段过滤。
  -> UserResponse 也能声明；两者同时写时，以 response_model 为准。
  过滤能挡住多余字段，但不是唯一安全措施，别靠它保管明文密码。

status / HTTP_201_CREATED / HTTP_204_NO_CONTENT
  语义化状态码常量，值仍是 201 / 204。
  204 不要再返回 JSON Body。

PUT vs PATCH
  PUT 偏向完整替换；PATCH 偏向部分修改。公司约定可能不同。

exclude_unset=True
  dump 时丢掉「模型有默认值、但客户端没提交」的字段。
  PATCH 只改 name 时，email 才不会被默认 None 盖掉。
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v17 notes 运行完毕 ---")
