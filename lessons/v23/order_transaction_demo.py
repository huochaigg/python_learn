"""下单原子性：失败不留半成品，成功则订单+明细+库存一起生效。

运行（项目根目录）：
uv run python -m lessons.v23.order_transaction_demo
"""

from sqlalchemy import func, select

from lessons.v23.app.database import SessionLocal, init_db
from lessons.v23.app.exceptions.business import InsufficientStockError
from lessons.v23.app.models.order import Order
from lessons.v23.app.models.order_item import OrderItem
from lessons.v23.app.models.stock import Stock
from lessons.v23.app.schemas.order import OrderCreate, OrderItemCreate
from lessons.v23.app.services.order_service import OrderService
from lessons.v23.seed import seed


def show(title: str) -> dict[str, int]:
    session = SessionLocal()
    try:
        stocks = {
            row.sku: row.quantity
            for row in session.execute(select(Stock).order_by(Stock.sku)).scalars()
        }
        orders = list(session.execute(select(Order).order_by(Order.id)).scalars())
        items = int(session.scalar(select(func.count()).select_from(OrderItem)) or 0)
        print(f"\n===== {title} =====")
        print("stocks:", stocks)
        print("orders:", [(row.id, row.order_no, row.total_amount) for row in orders])
        print("order_items count:", items)
        return stocks
    finally:
        session.close()


def create(service: OrderService, data: OrderCreate) -> None:
    # 每次新 Session：create_order 用 with session.begin() 作为事务边界。
    # 同一 Session 若已经 autobegin（例如刚查询过），再 begin() 会冲突。
    session = SessionLocal()
    try:
        service.create_order(session, data)
    finally:
        session.close()


def main() -> None:
    init_db()
    seed()
    service = OrderService()

    before = show("before fail order")
    try:
        # A001 够，B001 不够。_deduct_stock 可能先扣 A001，再在 B001 raise。
        create(
            service,
            OrderCreate(
                order_no="FAIL-A-AND-B",
                items=[
                    OrderItemCreate(sku="A001", quantity=2, price=10),
                    OrderItemCreate(sku="B001", quantity=999, price=5),
                ],
            ),
        )
    except InsufficientStockError as exc:
        print("caught InsufficientStockError:", exc)

    after_fail = show("after fail (must match before: no partial stock, no half order)")
    assert after_fail == before

    create(
        service,
        OrderCreate(
            order_no="OK-A-AND-C",
            items=[
                OrderItemCreate(sku="A001", quantity=2, price=10),
                OrderItemCreate(sku="C001", quantity=1, price=7),
            ],
        ),
    )
    after_ok = show("after success (A001-2, C001-1, order+items exist)")
    assert after_ok["A001"] == before["A001"] - 2
    assert after_ok["B001"] == before["B001"]
    assert after_ok["C001"] == before["C001"] - 1

    session = SessionLocal()
    try:
        assert session.execute(select(Order).where(Order.order_no == "FAIL-A-AND-B")).scalar_one_or_none() is None
        order = session.execute(select(Order).where(Order.order_no == "OK-A-AND-C")).scalar_one()
        item_count = session.scalar(
            select(func.count()).select_from(OrderItem).where(OrderItem.order_id == order.id)
        )
        assert item_count == 2
    finally:
        session.close()
    print("atomicity checks passed")


if __name__ == "__main__":
    main()
    print("\n--- v23 order_transaction_demo 运行完毕 ---")
