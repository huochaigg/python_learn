"""原子 UPDATE 扣库存；多 SKU 仍用 V23 事务包起来。"""

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from lessons.v24.app.exceptions.business import (
    DuplicateOrderNoError,
    InsufficientStockError,
    StockNotFoundError,
)
from lessons.v24.app.models.order import Order
from lessons.v24.app.models.order_item import OrderItem
from lessons.v24.app.models.stock import Stock
from lessons.v24.app.schemas.order import OrderCreate


def atomic_deduct(session: Session, sku: str, qty: int) -> None:
    # sqlalchemy.update()：构造 SQL UPDATE statement。
    # 和「先查出 ORM 对象 → 改 Python 属性 → flush」不是同一条路。
    # 不要用 f-string 拼 SQL。
    #
    # Stock.quantity - qty：SQL Expression，让数据库执行 quantity = quantity - :qty，
    # 不是先在 Python 内存读出 quantity 再算。
    #
    # WHERE sku=? AND quantity>=?：判断够不够 + 扣减写在同一条 UPDATE 里，
    # 关掉经典「先 SELECT 再 UPDATE」之间的竞争窗口。
    stmt = (
        update(Stock)
        .where(Stock.sku == sku, Stock.quantity >= qty)
        .values(quantity=Stock.quantity - qty)
    )
    result = session.execute(stmt)
    # rowcount：这条单行 UPDATE 匹配了多少行。
    # 1=扣减成功；0=条件没命中（sku 不存在，或库存不够）。
    # 官方提醒：RETURNING / executemany / 某些 DBAPI 下 rowcount 可能不可靠，
    # 不要推广成「所有 SQL 都能靠 rowcount 判断」。
    if result.rowcount == 1:
        return
    stock = session.execute(select(Stock).where(Stock.sku == sku)).scalar_one_or_none()
    if stock is None:
        raise StockNotFoundError(sku)
    raise InsufficientStockError(sku, stock.quantity, qty)


class OrderService:
    def list_stocks(self, session: Session) -> list[Stock]:
        return list(session.execute(select(Stock).order_by(Stock.sku.asc())).scalars().all())

    def list_orders(self, session: Session) -> list[Order]:
        return list(session.execute(select(Order).order_by(Order.id.asc())).scalars().all())

    def get_stock(self, session: Session, sku: str) -> Stock:
        stock = session.execute(select(Stock).where(Stock.sku == sku)).scalar_one_or_none()
        if stock is None:
            raise StockNotFoundError(sku)
        return stock

    def deduct_atomic(self, session: Session, sku: str, qty: int) -> Stock:
        # 原子 UPDATE 仍在事务里。单 SKU 用 begin 包住；多 SKU 见 create_order_atomic。
        with session.begin():
            atomic_deduct(session, sku, qty)
        return self.get_stock(session, sku)

    def deduct_pessimistic_demo(self, session: Session, sku: str, qty: int) -> Stock:
        # 教学/实验：练习 with_for_update() API。
        # SQLite 不能当成 MySQL/PostgreSQL 行锁等待的真实证据。
        with session.begin():
            stmt = select(Stock).where(Stock.sku == sku).with_for_update()
            stock = session.execute(stmt).scalar_one_or_none()
            if stock is None:
                raise StockNotFoundError(sku)
            if stock.quantity < qty:
                raise InsufficientStockError(sku, stock.quantity, qty)
            stock.quantity -= qty
        return self.get_stock(session, sku)

    def create_order_atomic(self, session: Session, data: OrderCreate) -> Order:
        # 原子 UPDATE 解决「单条库存」的并发判断；
        # 多个 SKU 仍要 V23 事务保证整单原子性：一个失败全部 rollback。
        try:
            with session.begin():
                order = Order(
                    order_no=data.order_no,
                    status="pending",
                    total_amount=sum(row.price * row.quantity for row in data.items),
                )
                session.add(order)
                session.flush()
                for row in data.items:
                    atomic_deduct(session, row.sku, row.quantity)
                    session.add(
                        OrderItem(
                            order_id=order.id,
                            sku=row.sku,
                            quantity=row.quantity,
                            price=row.price,
                        )
                    )
        except IntegrityError as exc:
            raise DuplicateOrderNoError(data.order_no) from exc
        return order
