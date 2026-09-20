"""原子 UPDATE：WHERE quantity >= need，用 rowcount 判断成败。

运行（项目根目录）：
uv run python -m lessons.v24.atomic_update_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker

from lessons.v24.app.exceptions.business import InsufficientStockError
from lessons.v24.app.models.base import Base
from lessons.v24.app.models.order import Order
from lessons.v24.app.models.stock import Stock
from lessons.v24.app.schemas.order import OrderCreate, OrderItemCreate
from lessons.v24.app.services.order_service import OrderService, atomic_deduct

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "atomic_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def snapshot(title: str) -> dict[str, int]:
    session = SessionLocal()
    try:
        stocks = {
            row.sku: row.quantity
            for row in session.execute(select(Stock).order_by(Stock.sku)).scalars()
        }
        orders = [row.order_no for row in session.execute(select(Order)).scalars()]
        print(f"{title}: stocks={stocks} orders={orders}")
        return stocks
    finally:
        session.close()


def reset() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add_all(
            [
                Stock(sku="A001", quantity=10, version_id=1),
                Stock(sku="B001", quantity=20, version_id=1),
                Stock(sku="C001", quantity=5, version_id=1),
            ]
        )
        session.commit()
    finally:
        session.close()


def demo_single_update() -> None:
    print("\n===== single SKU atomic UPDATE =====")
    session = SessionLocal()
    try:
        with session.begin():
            atomic_deduct(session, "A001", 3)
        print("deduct 3 from A001 ok")
    finally:
        session.close()
    snapshot("after A001-3")

    session = SessionLocal()
    try:
        with session.begin():
            atomic_deduct(session, "A001", 999)
    except InsufficientStockError as exc:
        print("expected fail:", exc)
    finally:
        session.close()
    snapshot("after A001-999 fail (A001 unchanged from previous success)")


def demo_multi_sku_transaction() -> None:
    print("\n===== multi SKU: A/B enough, C not; whole tx rollback =====")
    service = OrderService()
    before = snapshot("before fail order")
    session = SessionLocal()
    try:
        service.create_order_atomic(
            session,
            OrderCreate(
                order_no="FAIL-C",
                items=[
                    OrderItemCreate(sku="A001", quantity=1, price=10),
                    OrderItemCreate(sku="B001", quantity=1, price=5),
                    OrderItemCreate(sku="C001", quantity=999, price=7),
                ],
            ),
        )
    except InsufficientStockError as exc:
        print("caught:", exc)
    finally:
        session.close()
    after = snapshot("after fail")
    assert after == before

    print("\n===== multi SKU success =====")
    session = SessionLocal()
    try:
        service.create_order_atomic(
            session,
            OrderCreate(
                order_no="OK-ABC",
                items=[
                    OrderItemCreate(sku="A001", quantity=1, price=10),
                    OrderItemCreate(sku="B001", quantity=2, price=5),
                    OrderItemCreate(sku="C001", quantity=1, price=7),
                ],
            ),
        )
    finally:
        session.close()
    ok = snapshot("after success")
    assert ok["A001"] == before["A001"] - 1
    assert ok["B001"] == before["B001"] - 2
    assert ok["C001"] == before["C001"] - 1


def main() -> None:
    reset()
    snapshot("start A001=10 B001=20 C001=5")
    demo_single_update()
    demo_multi_sku_transaction()
    print("atomicity + atomic UPDATE checks passed")


if __name__ == "__main__":
    main()
    print("\n--- v24 atomic_update_demo 运行完毕 ---")
