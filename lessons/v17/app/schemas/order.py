"""订单 Request / Response Schema。和 users Schema 独立存放，观察多模块拆分。"""

from typing import Literal

from pydantic import BaseModel, Field

# Literal：把取值收窄到几个字面量，给检查器和 OpenAPI 用。
# 这里表示订单状态只允许这三种字符串，不是再讲一遍 V10。
type OrderStatus = Literal["pending", "paid", "cancelled"]


class OrderCreate(BaseModel):
    user_id: int
    amount: int = Field(ge=0)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    status: OrderStatus
