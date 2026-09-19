"""手动事务：try 里改两份数据，第二步失败则 rollback 再 raise。

运行（项目根目录）：
uv run python -m lessons.v23.transaction_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from lessons.v23.app.models.base import Base
from lessons.v23.app.models.stock import Stock

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "transaction_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def snapshot(title: str) -> dict[str, int]:
    session = SessionLocal()
    try:
        rows = {
            row.sku: row.quantity
            for row in session.execute(select(Stock).order_by(Stock.sku)).scalars()
        }
        print(f"{title}: {rows}")
        return rows
    finally:
        session.close()


def seed_demo() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        if session.scalar(select(Stock.id).limit(1)) is not None:
            return
        session.add_all([Stock(sku="A001", quantity=10), Stock(sku="B001", quantity=20)])
        session.commit()
    finally:
        session.close()


def try_two_updates_then_fail() -> None:
    # Transaction：多个数据库操作组成一个原子工作单元。
    # 正常全部 commit；任意步骤失败则 rollback。重点消灭「部分成功」。
    #
    # 默认 autobegin：第一次真正碰数据库时，Session 通常会自动进入事务。
    # 所以这里即使没写 begin()，下面的修改也在一个事务里，直到 commit/rollback。
    session = SessionLocal()
    try:
        a = session.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
        b = session.execute(select(Stock).where(Stock.sku == "B001")).scalar_one()
        print(f"in session before change: A001={a.quantity} B001={b.quantity}")
        a.quantity -= 1
        print("step1: A001 -= 1 (pending in current transaction, not final)")
        raise RuntimeError("step2 failed on purpose")
        b.quantity -= 1
        session.commit()
    except Exception:
        # rollback()：撤销「当前尚未提交」事务里的数据库修改。
        # 不会撤销之前已经 commit 的事务。
        session.rollback()
        raise
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    seed_demo()
    snapshot("before")
    try:
        try_two_updates_then_fail()
    except RuntimeError as exc:
        print("caller caught after rollback+raise:", exc)
    snapshot("after rollback (A001 must still be 10)")


if __name__ == "__main__":
    main()
    print("\n--- v23 transaction_demo 运行完毕 ---")
