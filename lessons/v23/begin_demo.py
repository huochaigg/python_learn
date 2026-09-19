"""用 with session.begin() 重写手动事务 Demo（对照 V6 Context Manager）。

运行（项目根目录）：
uv run python -m lessons.v23.begin_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from lessons.v23.app.models.base import Base
from lessons.v23.app.models.stock import Stock

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "begin_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def snapshot(title: str) -> None:
    session = SessionLocal()
    try:
        rows = {
            row.sku: row.quantity
            for row in session.execute(select(Stock).order_by(Stock.sku)).scalars()
        }
        print(f"{title}: {rows}")
    finally:
        session.close()


def seed_demo() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add_all([Stock(sku="A001", quantity=10), Stock(sku="B001", quantity=20)])
        session.commit()
    finally:
        session.close()


def try_two_updates_then_fail() -> None:
    session = SessionLocal()
    try:
        # Session.begin()：显式开启/划定一个事务范围。
        # with 进入 = 进入事务范围（对照 V6 Context Manager 的 __enter__）。
        # 正常退出 = commit；异常退出 = rollback，然后异常继续传播。
        # 不要在 begin() 之前先查询：默认 autobegin 可能已经打开事务。
        with session.begin():
            a = session.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
            b = session.execute(select(Stock).where(Stock.sku == "B001")).scalar_one()
            a.quantity -= 1
            print("step1: A001 -= 1 inside begin(), not committed yet")
            raise RuntimeError("step2 failed on purpose")
            b.quantity -= 1
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    seed_demo()
    snapshot("before")
    try:
        try_two_updates_then_fail()
    except RuntimeError as exc:
        print("caller caught after begin() auto-rollback+raise:", exc)
    snapshot("after (A001 must still be 10)")


if __name__ == "__main__":
    main()
    print("\n--- v23 begin_demo 运行完毕 ---")
