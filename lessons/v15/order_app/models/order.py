"""订单模型。"""

from dataclasses import dataclass, field
from typing import Literal

from lessons.v15.order_app.models.user import UserId

type OrderId = int
type OrderStatus = Literal["pending", "paid", "cancelled"]


@dataclass
class OrderItem:
    sku: str
    qty: int
    unit_price: int


@dataclass
class Order:
    id: OrderId
    user_id: UserId
    status: OrderStatus
    total_amount: int
    # field(default_factory=list)：每个实例各自一份新 list，避免共享可变默认值。
    # 不要写 items: list[OrderItem] = []。这和 V3 函数默认参数不要用 [] 是同一类坑。
    items: list[OrderItem] = field(default_factory=list)
