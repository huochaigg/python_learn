"""HTTP Schema。UserQuery 是请求查询条件，不是数据库 ORM Model。"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserQuery(BaseModel):
    """GET /users 的 Query 参数模型（FastAPI Class Dependency）。

    第一次用 Pydantic 承接查询参数：它只描述 HTTP 筛选条件
    （?keyword=&active=&page=），不是 SQLAlchemy ORM Model，也不会建表。
    Router 用 Annotated[UserQuery, Query()] 把它拆成一组 Query，
    避免 endpoint 函数参数列表无限膨胀。
    """

    keyword: str | None = Field(default=None, max_length=50)
    active: bool | None = None
    min_age: int | None = Field(default=None, ge=0, le=150)
    max_age: int | None = Field(default=None, ge=0, le=150)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=50)
    sort_by: Literal["id", "name", "age", "created_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int
    active: bool
    created_at: datetime


class UserPageResponse(BaseModel):
    """单表列表分页响应。先用具体类型，不引入 Generic Page[T]。"""

    items: list[UserResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
