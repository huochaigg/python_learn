"""flush 能拿到数据库生成的 id，但不是 commit。rollback 仍可撤销。

运行（项目根目录）：
uv run python -m lessons.v23.flush_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker

from lessons.v23.app.models.base import Base
from lessons.v23.app.models.order import Order
from lessons.v23.app.models.order_item import OrderItem

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "flush_demo.db"
# echo=True 方便看见 INSERT 已经发出，随后 ROLLBACK。
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


def count_orders() -> int:
    session = SessionLocal()
    try:
        return int(session.scalar(select(func.count()).select_from(Order)) or 0)
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    print("orders before =", count_orders())

    session = SessionLocal()
    try:
        order = Order(order_no="FLUSH-1", status="pending", total_amount=10)
        session.add(order)
        print("after add, order.id =", order.id, "(usually None, SQL not sent yet)")

        # flush()：把 Session 当前 pending changes 同步到数据库，INSERT/UPDATE 会执行，
        # 因此能拿到数据库生成的 order.id。但它不会最终提交事务，不是「小型 commit」。
        # 后面 rollback 仍然可以撤销这些修改。
        # 普通简单 CRUD 通常不用手动 flush：commit() 在真正提交前会先无条件 flush。
        # 手动 flush 常见于：还不能提交，但后续已经需要 id / 约束结果。
        session.flush()
        print("after flush, order.id =", order.id, "(SQL ran, transaction NOT committed)")

        session.add(
            OrderItem(order_id=order.id, sku="A001", quantity=1, price=10)
        )
        raise RuntimeError("fail after flush on purpose")
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print("caught after rollback+raise:", exc)
    print("orders after rollback =", count_orders(), "(must be 0)")
    print("\n--- v23 flush_demo 运行完毕 ---")
