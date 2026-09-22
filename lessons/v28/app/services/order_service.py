from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.order import Order
from ..models.order_item import OrderItem
from ..schemas.order import OrderCreate


class DuplicateOrderNoError(Exception):
    def __init__(self, order_no: str) -> None:
        self.order_no = order_no
        super().__init__(order_no)


class OrderService:
    async def get_order(self, session: AsyncSession, order_id: int) -> Order | None:
        # selectinload：async ORM 应避免关系属性在普通访问时偷偷触发隐式 IO。
        # 需要关系数据时优先在 SELECT 阶段明确 eager load，不要等 Pydantic 序列化时再查。
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    async def list_orders(self, session: AsyncSession) -> list[Order]:
        stmt = select(Order).options(selectinload(Order.items)).order_by(Order.id.asc())
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def create_order(self, session: AsyncSession, data: OrderCreate) -> Order:
        total = sum(item.quantity * item.price for item in data.items)
        try:
            # 对照 V23：事务语义完全没变，只是进入/退出和数据库操作采用 async API；
            # 异常离开事务块时自动 rollback。内部不要再自行 commit。
            async with session.begin():
                order = Order(order_no=data.order_no, status="pending", total_amount=total)
                session.add(order)
                await session.flush()
                for item in data.items:
                    session.add(
                        OrderItem(
                            order_id=order.id,
                            sku=item.sku,
                            quantity=item.quantity,
                            price=item.price,
                        )
                    )
        except IntegrityError as extra:
            await session.rollback()
            raise DuplicateOrderNoError(data.order_no) from extra
        loaded = await self.get_order(session, order.id)
        assert loaded is not None
        return loaded
