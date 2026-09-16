"""用户 Request / Response Schema。要分开，不要拿同一份模型既收密码又对外返回。"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """创建用户的请求体。客户端提交什么，就按这个校验。"""

    name: str = Field(min_length=1, max_length=50)
    email: str
    # password 只出现在 Request Schema。UserResponse 故意没有这个字段。
    # 本课不 Hash；正式项目也不该把明文密码传来传去、打日志。
    password: str = Field(min_length=1, description="只用于创建，不会出现在响应里")


class UserUpdate(BaseModel):
    """PATCH 部分更新。字段都可以不传。

    str | None：值允许是 None（V10）。
    = None：参数/字段有默认值，客户端可以省略。
    客户端「有没有提交过这个键」，还要靠 Pydantic 字段状态；
    更新时用 model_dump(exclude_unset=True)，别把没提交的字段用默认 None 盖掉。
    """

    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = None


class UserPut(BaseModel):
    """PUT 完整替换用的公开字段（本课不替换 password）。"""

    name: str = Field(min_length=1, max_length=50)
    email: str


class UserResponse(BaseModel):
    """对外响应。没有 password。

    Request Schema 负责「收什么」；Response Schema 负责「露出什么」。
    NestJS 对照：CreateUserDto 和 UserEntity/ResponseDto 分开，不是同一个 class。
    """

    id: int
    name: str
    email: str
