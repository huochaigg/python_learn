"""创建订单 + 明细 + 扣库存：一个事务。内部方法不许自己 commit。"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from lessons.v23.app.exceptions.business import (
    DuplicateOrderNoError,
    InsufficientStockError,
    InvalidOrderError,
    StockNotFoundError,
)
from lessons.v23.app.models.order import Order
from lessons.v23.app.models.order_item import OrderItem
from lessons.v23.app.models.stock import Stock
from lessons.v23.app.schemas.order import OrderCreate, OrderItemCreate


class OrderService:
    def create_order(self, session: Session, data: OrderCreate) -> Order:
        # Transaction：把多个数据库操作组成一个原子工作单元。
        # 正常全部 commit；任意步骤失败则 rollback。用来消灭「部分成功」。
        #
        # Session.begin()：显式划定事务范围。with 正常退出 commit，
        # 异常退出 rollback，然后异常继续传播（V6 Context Manager）。
        # 「创建订单 + 创建明细 + 扣库存」是一个完整业务动作，必须共享
        # 这一个 transaction boundary，而不是每个小函数自己 commit。
        #
        # 全部数据库读写都放进 begin() 内：默认 autobegin 下，如果先查询
        # 再调用 begin()，Session 可能已经在事务里，会报错。
        try:
            with session.begin():
                self._validate_items(data.items)
                order = Order(
                    order_no=data.order_no,
                    status="pending",
                    total_amount=sum(row.price * row.quantity for row in data.items),
                )
                session.add(order)
                # flush：把 Session 里 pending changes 发到数据库（INSERT 会执行），
                # 因而能拿到数据库生成的 order.id。flush 不是小型 commit：
                # 事务尚未拍板，后面 rollback 仍可撤销。普通 CRUD 不必手动 flush，
                # 因为 commit() 提交前会先无条件 flush。
                # 这里还不能 commit：明细和扣库存还没做完。
                session.flush()
                self._create_items(session, order, data.items)
                self._deduct_stock(session, data.items)
        except IntegrityError as exc:
            # begin() 在异常退出时已经 rollback。转换成明确业务异常再 raise，
            # 不要 except Exception: rollback; return None，否则 V19 全局异常体系收不到真实错误。
            raise DuplicateOrderNoError(data.order_no) from exc
        return order

    def list_orders(self, session: Session) -> list[Order]:
        return list(session.execute(select(Order).order_by(Order.id.asc())).scalars().all())

    def list_stocks(self, session: Session) -> list[Stock]:
        return list(session.execute(select(Stock).order_by(Stock.sku.asc())).scalars().all())

    def _validate_items(self, items: list[OrderItemCreate]) -> None:
        # 纯内存校验，不碰数据库，更不会 commit。真正事务边界仍在 create_order。
        if not items:
            raise InvalidOrderError("items must not be empty")

    def _create_items(
        self,
        session: Session,
        order: Order,
        items: list[OrderItemCreate],
    ) -> None:
        # 参与外层事务，自己不 commit。需要主键时只 flush。
        for row in items:
            session.add(
                OrderItem(
                    order_id=order.id,
                    sku=row.sku,
                    quantity=row.quantity,
                    price=row.price,
                )
            )

    def _deduct_stock(self, session: Session, items: list[OrderItemCreate]) -> None:
        # 逐个扣减：A001 可能先改内存/发 UPDATE，B001 再 raise。
        # 异常会离开 with session.begin()，整笔事务 rollback，A001 也不会留下扣减。
        # 不要在这里 catch 后吞掉。
        for row in items:
            stock = session.execute(
                select(Stock).where(Stock.sku == row.sku)
            ).scalar_one_or_none()
            if stock is None:
                raise StockNotFoundError(row.sku)
            if stock.quantity < row.quantity:
                raise InsufficientStockError(row.sku, stock.quantity, row.quantity)
            stock.quantity -= row.quantity
