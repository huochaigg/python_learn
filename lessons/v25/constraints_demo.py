"""
文件作用：演示数据库四类约束：UNIQUE / NOT NULL / CHECK / ForeignKey。
重点概念：unique=True、nullable=False、CheckConstraint、约束名、FK + SQLite PRAGMA。
观察重点：第二次插入如何被数据库拒绝；异常类型是 IntegrityError，不要把内部 SQL 当业务文案。
"""

from pathlib import Path

from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from lessons.v25.app.models.base import Base
from lessons.v25.app.models.order import Order
from lessons.v25.app.models.order_item import OrderItem
from lessons.v25.app.models.stock import Stock
from lessons.v25.app.models.user import User

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "constraints_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def reset() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)


def demo_unique() -> None:
    print("\n===== demo_unique =====")
    session = SessionLocal()
    try:
        session.add(User(name="Ada", email="ada@example.com"))
        session.commit()
        print("first insert ok")
        session.add(User(name="Ada2", email="ada@example.com"))
        session.commit()
    except IntegrityError as exc:
        print("second insert blocked:", type(exc).__name__)
        print("do not return database errmsg to client")
        session.rollback()
    finally:
        session.close()


def demo_not_null() -> None:
    print("\n===== demo_not_null =====")
    session = SessionLocal()
    try:
        session.add(User(name=None, email="null-name@example.com"))
        session.commit()
    except IntegrityError as exc:
        print("NOT NULL blocked:", type(exc).__name__)
        session.rollback()
    finally:
        session.close()


def demo_check_constraint() -> None:
    print("\n===== demo_check_constraint =====")
    session = SessionLocal()
    try:
        session.add(Stock(sku="A001", quantity=1))
        session.commit()
        print("quantity=1 ok")
        session.add(Stock(sku="BAD", quantity=-1))
        session.commit()
    except IntegrityError as exc:
        print("CHECK ck_stock_quantity_non_negative blocked:", type(exc).__name__)
        session.rollback()
    finally:
        session.close()


def demo_foreign_key() -> None:
    print("\n===== demo_foreign_key =====")
    session = SessionLocal()
    try:
        session.add(
            OrderItem(order_id=99999, sku="A001", quantity=1, price=10)
        )
        session.commit()
    except IntegrityError as extra:
        print("FK blocked, parent order 99999 does not exist:", type(extra).__name__)
        session.rollback()
    finally:
        session.close()

    session = SessionLocal()
    try:
        order = Order(
            order_no="ORD-1",
            status="pending",
            total_amount=10,
            idempotency_key="key-1",
        )
        session.add(order)
        session.flush()
        session.add(OrderItem(order_id=order.id, sku="A001", quantity=1, price=10))
        session.commit()
        print("FK ok when parent exists, item count =", session.scalar(select(OrderItem.id).limit(1)))
    finally:
        session.close()


def main() -> None:
    reset()
    demo_unique()
    demo_not_null()
    demo_check_constraint()
    demo_foreign_key()


if __name__ == "__main__":
    main()
    print("\n--- v25 constraints_demo 运行完毕 ---")
