"""
文件作用：学习幂等，不是完整支付系统。看 Idempotency-Key + UNIQUE 如何防止重复创建。
重点概念：幂等 Key、先查再插的并发窗口、UNIQUE 兜底、相同 key 只留一单。
观察重点：同一 key 两次调用只有一条 Order；不同 key 可以创建两单。
"""

from pathlib import Path

from sqlalchemy import create_engine, event, func, select
from sqlalchemy.orm import sessionmaker

from lessons.v25.app.models.base import Base
from lessons.v25.app.models.order import Order
from lessons.v25.app.schemas.order import OrderCreate, OrderItemCreate
from lessons.v25.app.services.order_service import create_order_idempotent

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "idempotency_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def count_orders() -> int:
    session = SessionLocal()
    try:
        return int(session.scalar(select(func.count()).select_from(Order)) or 0)
    finally:
        session.close()


def demo_same_key() -> None:
    print("\n===== same Idempotency-Key twice =====")
    body = OrderCreate(
        order_no="ORD-SAME",
        items=[OrderItemCreate(sku="A001", quantity=1, price=10)],
    )
    session = SessionLocal()
    try:
        first = create_order_idempotent(session, "pay-001", body)
        second = create_order_idempotent(session, "pay-001", body)
        print("first id", first.id, "second id", second.id, "same object/row?", first.id == second.id)
    finally:
        session.close()
    print("order count after two same-key calls =", count_orders())


def demo_different_keys() -> None:
    print("\n===== two different keys =====")
    session = SessionLocal()
    try:
        a = create_order_idempotent(
            session,
            "pay-aaa",
            OrderCreate(
                order_no="ORD-A",
                items=[OrderItemCreate(sku="A001", quantity=1, price=10)],
            ),
        )
        b = create_order_idempotent(
            session,
            "pay-bbb",
            OrderCreate(
                order_no="ORD-B",
                items=[OrderItemCreate(sku="B001", quantity=1, price=20)],
            ),
        )
        print("created two orders", a.id, b.id, a.idempotency_key, b.idempotency_key)
    finally:
        session.close()
    print("order count =", count_orders())


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    demo_same_key()
    demo_different_keys()


if __name__ == "__main__":
    main()
    print("\n--- v25 idempotency_demo 运行完毕 ---")
