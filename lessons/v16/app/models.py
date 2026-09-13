"""V16 请求 Body 用的 Pydantic 模型（DTO）。"""

from pydantic import BaseModel, Field


# BaseModel：Pydantic 的数据模型基类。
# 用途：声明外部 JSON 的形状，并在运行时做解析、校验、序列化。
# FastAPI 看到函数参数类型是 BaseModel 子类时，通常把它当成 Request Body。
# 和 V8 dataclass 不同：dataclass 更偏进程内数据对象；BaseModel 更偏 API DTO。
# NestJS 对照：接近 DTO + class-validator + class-transformer 的一部分能力，不是完全等价。
class UserCreate(BaseModel):
    # Field(...)：给 Pydantic 字段加校验规则和 OpenAPI metadata（description 等）。
    # 用途：Body 里的约束写在模型字段上；Query/Path 的约束则用 Query()/Path()。
    # 常见坑：不要把 Field 和 FastAPI 的 Query/Path 混用在同一层含义上。
    name: str = Field(min_length=1, max_length=50, description="用户名")
    age: int = Field(ge=0, le=150, description="年龄，必须能转成 int 且 >= 0")
    email: str
    active: bool = True


class UserUpdate(BaseModel):
    # 可选字段：类型允许 None，并且给了 = None，调用方才能省略。
    # 只有 str | None 没有默认值时，JSON 里仍然通常必须出现这个键（或显式 null，视配置而定）。
    name: str | None = Field(default=None, min_length=1, max_length=50)
    age: int | None = Field(default=None, ge=0, le=150)
    email: str | None = None
    active: bool | None = None
