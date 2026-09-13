"""订单业务：创建、查询、取消、并发详情、限流批量、状态流。"""

import asyncio
import time
from collections.abc import AsyncIterator, Iterator

from lessons.v15.order_app.exceptions import (
    InsufficientStockError,
    InvalidOrderStatusError,
    OrderNotFoundError,
    UserNotFoundError,
)
from lessons.v15.order_app.models.order import Order, OrderId, OrderItem
from lessons.v15.order_app.models.user import UserId
from lessons.v15.order_app.repositories.order_repository import OrderRepository
from lessons.v15.order_app.repositories.user_repository import UserRepository
from lessons.v15.order_app.utils.decorators import log_execution, measure_time, require_role


class OrderService:
    def __init__(
        self,
        orders: OrderRepository,
        users: UserRepository,
        stock: dict[str, int],
    ) -> None:
        # 手动 constructor 注入：main 创建 Repository / stock，再传给 Service。
        # FastAPI Depends、NestJS constructor injection 是同一思想的框架版。
        self._orders = orders
        self._users = users
        self._stock = stock

    @log_execution
    def compute_total(self, items: list[OrderItem]) -> int:
        return sum(item.qty * item.unit_price for item in items)

    async def create_order(self, user_id: UserId, items: list[OrderItem]) -> Order:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"user not found: {user_id}")
        for item in items:
            left = self._stock.get(item.sku, 0)
            if item.qty > left:
                raise InsufficientStockError(
                    f"sku={item.sku} left={left} need={item.qty}"
                )
        total = self.compute_total(items)
        for item in items:
            self._stock[item.sku] -= item.qty
        draft = Order(
            id=0,
            user_id=user_id,
            status="pending",
            total_amount=total,
            items=list(items),
        )
        return await self._orders.create(draft)

    async def get_order(self, order_id: OrderId) -> Order:
        order = await self._orders.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(f"order not found: {order_id}")
        return order

    async def list_orders(self) -> list[Order]:
        return await self._orders.list_all()

    @require_role("admin")
    async def cancel_order(self, order_id: OrderId, *, current_role: str = "guest") -> Order:
        order = await self.get_order(order_id)
        if order.status != "pending":
            raise InvalidOrderStatusError(f"cannot cancel status={order.status}")
        order.status = "cancelled"
        return await self._orders.update(order)

    async def _fetch_user_profile(self, user_id: UserId) -> dict[str, str | int]:
        await asyncio.sleep(0.12)
        user = await self._users.get_by_id(user_id)
        name = user.name if user else "unknown"
        return {"user_id": user_id, "name": name}

    async def _fetch_stock_snapshot(self, order: Order) -> dict[str, int]:
        await asyncio.sleep(0.10)
        return {item.sku: self._stock.get(item.sku, 0) for item in order.items}

    async def _fetch_shipping(self, order_id: OrderId) -> dict[str, str | int]:
        await asyncio.sleep(0.08)
        return {"order_id": order_id, "carrier": "SF", "tracking": f"SF-{order_id:04d}"}

    @measure_time
    async def get_order_detail(self, order_id: OrderId, *, concurrent: bool = True) -> dict:
        """详情需要用户 / 库存 / 物流三份独立 IO。

        asyncio.gather()：同时推进多个 awaitable，全部完成后按传入顺序返回。
        JS 对比：使用场景接近 Promise.all。不是多线程，只是一起等 IO。
        """
        order = await self.get_order(order_id)
        user_job = self._fetch_user_profile(order.user_id)
        stock_job = self._fetch_stock_snapshot(order)
        ship_job = self._fetch_shipping(order.id)
        if concurrent:
            user_info, stock_info, shipping = await asyncio.gather(
                user_job, stock_job, ship_job
            )
        else:
            user_info = await user_job
            stock_info = await stock_job
            shipping = await ship_job
        return {
            "order": order,
            "user": user_info,
            "stock": stock_info,
            "shipping": shipping,
        }

    async def get_many(self, order_ids: list[OrderId]) -> list[Order]:
        # Semaphore(3)：当前进程内最多 3 个查询同时进入。
        # 它不是 Redis / BullMQ 那种可靠任务队列：重启就没了，也不跨 Worker。
        limiter = asyncio.Semaphore(3)

        async def fetch_one(order_id: OrderId) -> Order:
            async with limiter:
                print(f"  start order={order_id} t={time.perf_counter():.2f}")
                order = await self.get_order(order_id)
                print(f"  end   order={order_id} t={time.perf_counter():.2f}")
                return order

        return list(await asyncio.gather(*[fetch_one(oid) for oid in order_ids]))

    async def stream_order_status(self, order_id: OrderId) -> AsyncIterator[str]:
        """Async Generator：async def + yield。调用后得到 Async Generator Object。

        每隔一段时间 yield 一个物流状态。调用端必须 async for 消费，不能一次 await 完整个流。
        以后 FastAPI SSE / StreamingResponse / AI token streaming 就是这个模式加上网络协议。
        这里只模拟数据，不发 HTTP。
        """
        await self.get_order(order_id)
        for status in ("created", "processing", "shipped", "completed"):
            await asyncio.sleep(0.05)
            yield status

    def iter_summaries(self, orders: list[Order]) -> Iterator[str]:
        # 普通 Generator：按需产出摘要，不会一次性拼好所有字符串。
        for order in orders:
            yield f"#{order.id} {order.status} amount={order.total_amount}"


def iter_order_ids(start: OrderId, count: int) -> Iterator[OrderId]:
    """按需生成连续订单 ID，给批量查询当输入。"""
    for offset in range(count):
        yield start + offset
