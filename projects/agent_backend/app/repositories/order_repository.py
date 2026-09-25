from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order


class OrderRepository:
    async def get_by_order_no(self, session: AsyncSession, order_no: str) -> Order | None:
        stmt = select(Order).where(Order.order_no == order_no)
        return (await session.execute(stmt)).scalar_one_or_none()

    async def get_owned(
        self, session: AsyncSession, order_no: str, user_id: int
    ) -> Order | None:
        stmt = select(Order).where(Order.order_no == order_no, Order.user_id == user_id)
        return (await session.execute(stmt)).scalar_one_or_none()


order_repository = OrderRepository()
