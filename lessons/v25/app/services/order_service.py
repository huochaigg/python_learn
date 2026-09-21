"""幂等下单。先查 key + UNIQUE 并发兜底。"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from lessons.v25.app.exceptions.business import DataIntegrityError, OrderNotFoundError
from lessons.v25.app.models.order import Order
from lessons.v25.app.models.order_item import OrderItem
from lessons.v25.app.schemas.order import OrderCreate


def create_order_idempotent(
    session: Session,
    idempotency_key: str,
    data: OrderCreate,
) -> Order:
    existing = session.execute(
        select(Order).where(Order.idempotency_key == idempotency_key)
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    # 先查仍有并发窗口：A/B 都可能同时看不到这行。UNIQUE 必须保留。
    # 先 select 会 autobegin，后续用 commit/rollback，不要再套 begin()。
    order = Order(
        order_no=data.order_no,
        status="pending",
        total_amount=sum(row.price * row.quantity for row in data.items),
        idempotency_key=idempotency_key,
    )
    session.add(order)
    try:
        session.flush()
        for row in data.items:
            session.add(
                OrderItem(
                    order_id=order.id,
                    sku=row.sku,
                    quantity=row.quantity,
                    price=row.price,
                )
            )
        session.commit()
    except IntegrityError as extra:
        # 并发幂等兜底：两个 INSERT 撞 UNIQUE。rollback 后再按 key 读已成功的那一笔。
        session.rollback()
        found = session.execute(
            select(Order).where(Order.idempotency_key == idempotency_key)
        ).scalar_one_or_none()
        if found is not None:
            return found
        raise DataIntegrityError("order create conflict") from extra
    return order


class OrderService:
    def list_orders(self, session: Session) -> list[Order]:
        return list(session.execute(select(Order).order_by(Order.id.asc())).scalars().all())

    def get_by_key(self, session: Session, idempotency_key: str) -> Order:
        order = session.execute(
            select(Order).where(Order.idempotency_key == idempotency_key)
        ).scalar_one_or_none()
        if order is None:
            raise OrderNotFoundError(idempotency_key)
        return order

    def create_order_idempotent(
        self,
        session: Session,
        idempotency_key: str,
        data: OrderCreate,
    ) -> Order:
        return create_order_idempotent(session, idempotency_key, data)
