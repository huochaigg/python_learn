"""订单查询：Join / selectinload 都放这里，不进 Router。"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from lessons.v22.app.exceptions import OrderNotFoundError
from lessons.v22.app.models.order import Order
from lessons.v22.app.models.order_item import OrderItem
from lessons.v22.app.schemas.order import OrderCreate


class OrderService:
    def create_order(self, session: Session, data: OrderCreate) -> Order:
        order = Order(order_no=data.order_no, status=data.status)
        for row in data.items:
            # append 会同时填上 item.order（back_populates 双向同步）。
            # 默认 cascade save-update：add(order) 即可把子行一起纳入 Session。
            order.items.append(
                OrderItem(
                    sku=row.sku,
                    name=row.name,
                    price=row.price,
                    quantity=row.quantity,
                )
            )
        session.add(order)
        session.commit()
        return self.get_order_with_items(session, order.id)

    def get_order(self, session: Session, order_id: int) -> Order:
        order = session.get(Order, order_id)
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def get_order_with_items(self, session: Session, order_id: int) -> Order:
        # Response 含 items 时，查询阶段就要明确加载策略。
        # selectinload：eager loading。先查父对象，再用 WHERE order_id IN (...) 一次加载子集合。
        # 不要等 Pydantic 序列化访问 order.items 时才 Lazy Load。
        stmt = (
            select(Order)
            .where(Order.id == order_id)
            .options(selectinload(Order.items))
        )
        order = session.execute(stmt).scalar_one_or_none()
        if order is None:
            raise OrderNotFoundError(order_id)
        return order

    def list_orders(self, session: Session) -> list[Order]:
        stmt = select(Order).order_by(Order.id.asc())
        return list(session.execute(stmt).scalars().all())

    def list_orders_with_items(self, session: Session) -> list[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .order_by(Order.id.asc())
        )
        return list(session.execute(stmt).scalars().all())

    def find_orders_by_sku(self, session: Session, sku: str) -> list[Order]:
        # join(Order.items)：改的是这条查询本身，用来按子表条件过滤。
        # SQLAlchemy 根据 relationship / ForeignKey 推导 ON order_items.order_id = orders.id。
        # 这和 joinedload() 不是一回事：joinedload 是为了把 relationship 一起加载出来。
        stmt = (
            select(Order)
            .join(Order.items)
            .where(OrderItem.sku == sku)
            .options(selectinload(Order.items))
            .order_by(Order.id.asc())
        )
        # 一个订单多条 Item 都命中 sku 时，JOIN 结果里同一个 Order 会重复。
        # unique() 是 Result/ORM Entity 去重，不是 SQL DISTINCT。
        return list(session.execute(stmt).unique().scalars().all())
