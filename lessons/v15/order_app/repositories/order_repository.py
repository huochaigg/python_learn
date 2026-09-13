"""订单数据访问。内存 dict 模拟表，不是 SQLAlchemy。"""

import asyncio

from lessons.v15.order_app.models.order import Order, OrderId
from lessons.v15.order_app.repositories.session import FakeDatabaseSession


class OrderRepository:
    def __init__(self) -> None:
        self._store: dict[OrderId, Order] = {}
        self._next_id = 0

    async def create(self, order: Order) -> Order:
        self._next_id += 1
        saved = Order(
            id=self._next_id,
            user_id=order.user_id,
            status=order.status,
            total_amount=order.total_amount,
            items=list(order.items),
        )
        self._store[saved.id] = saved
        return saved

    async def get_by_id(self, order_id: OrderId) -> Order | None:
        # 查不到返回 None，不在这里 raise。业务语义留给 Service。
        # 这里用 sleep 模拟 IO，方便后面 Semaphore 观察并发上限。
        # 部分方法才会 async with FakeDatabaseSession（见 list_all）。
        await asyncio.sleep(0.08)
        return self._store.get(order_id)

    async def list_all(self) -> list[Order]:
        async with FakeDatabaseSession("orders") as _session:
            return list(self._store.values())

    async def update(self, order: Order) -> Order:
        self._store[order.id] = order
        return order
