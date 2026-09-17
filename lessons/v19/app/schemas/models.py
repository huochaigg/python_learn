"""HTTP 输入输出结构。异常 handler 主要用 dict，这个 Schema 只帮助看清字段。"""

from typing import Literal

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class OrderCreate(BaseModel):
    user_id: int
    sku: str
    qty: int = Field(ge=1)
    status: Literal["pending", "paid", "cancelled"] = "pending"


class OrderResponse(BaseModel):
    id: int
    user_id: int
    sku: str
    qty: int
    status: str


class ErrorResponse(BaseModel):
    """统一错误 body。handler 用 JSONResponse + dict，不必强行依赖这个模型。"""

    code: str
    message: str
    data: None = None
