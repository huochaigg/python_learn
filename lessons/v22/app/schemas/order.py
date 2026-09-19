"""HTTP Schema。能从 ORM 及 relationship 属性读数据，不是数据库表。"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=32)
    name: str = Field(min_length=1, max_length=80)
    price: int = Field(ge=0)
    quantity: int = Field(ge=1, le=99)


class OrderCreate(BaseModel):
    order_no: str = Field(min_length=1, max_length=32)
    status: str = Field(default="pending", max_length=20)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    sku: str
    name: str
    price: int
    quantity: int


class OrderSummaryResponse(BaseModel):
    """列表默认不带 items，避免无意触发 Lazy Load。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    status: str
    created_at: datetime


class OrderResponse(BaseModel):
    # from_attributes=True：可以从 ORM 对象属性（含 relationship）构造 Response。
    # 若 Schema 包含 items，Service 查询时就应明确加载策略，不要等序列化才 lazy SQL。
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    status: str
    created_at: datetime
    items: list[OrderItemResponse]
