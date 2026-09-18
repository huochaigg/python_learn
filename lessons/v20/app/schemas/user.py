"""Pydantic HTTP Schema。和 SQLAlchemy User 不是同一个 class。"""

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str
    age: int = Field(ge=0, le=150)
    nickname: str | None = None


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    nickname: str | None = None
    active: bool | None = None


class UserResponse(BaseModel):
    # ConfigDict(from_attributes=True)：允许从对象属性读数据，不只是 dict。
    # 这样 User ORM 实例可以直接变成 Response。Pydantic V1 的 orm_mode=True 是旧写法。
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    age: int
    active: bool
    nickname: str | None
