"""V16 NestJS -> FastAPI 认知映射（不是能力一一对应）。

运行：uv run python lessons/v16/notes.py
"""

NOTES = """
NestJS                         FastAPI（本课先这样记）
----------------------------   ---------------------------------
@Module + Controller 注册      FastAPI() 实例 + 路由装饰器注册
@Controller("users")           先写在一个 app 上；V17 再拆 APIRouter
@Get() / @Post()               @app.get() / @app.post()  （仍是 decorator，实现不同）
@Param("id")                   路由 {user_id} + 同名函数参数
@Query("page")                 不在 Path 里的简单类型，通常自动当 Query
@Body() + DTO                  参数类型写成 Pydantic BaseModel
class-validator / transformer  BaseModel + Field：解析、校验、序列化
@ApiProperty 等 Swagger 装饰器 类型 / Field / Query / Path 推 OpenAPI
GET /docs（要自己接 Swagger）  自带 /docs /redoc /openapi.json

只帮助迁移认知，不要当成 API 等价替换。

V16 要真正搞懂的 6 件事：
1. FastAPI 为什么能自动识别 Path / Query / Body
2. BaseModel 和 dataclass 差在哪
3. 类型标注为什么在 FastAPI 里有运行时作用
4. Annotated + Query/Path 在干什么
5. model_dump() 是干什么的
6. uvicorn lessons.v16.app.main:app 里 module:app 是什么意思
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v16 notes 运行完毕 ---")
