"""乐观锁：version_id_col。后提交的旧版本会 StaleDataError。

运行（项目根目录）：
uv run python -m lessons.v24.optimistic_lock_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import StaleDataError

from lessons.v24.app.exceptions.business import ConcurrencyConflictError
from lessons.v24.app.models.base import Base
from lessons.v24.app.models.stock import Stock

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "optimistic_demo.db"
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    setup = SessionLocal()
    try:
        setup.add(Stock(sku="A001", quantity=10, version_id=1))
        setup.commit()
    finally:
        setup.close()

    session_a = SessionLocal()
    session_b = SessionLocal()
    try:
        stock_a = session_a.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
        stock_b = session_b.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
        print(f"A loaded quantity={stock_a.quantity} version={stock_a.version_id}")
        print(f"B loaded quantity={stock_b.quantity} version={stock_b.version_id}")

        stock_a.quantity -= 1
        session_a.commit()
        print("A committed; version should increase")

        stock_b.quantity -= 1
        try:
            # B 仍拿着旧 version。flush/commit 的 UPDATE 带 WHERE version_id=:old。
            # StaleDataError：ORM 预期更新某行，但版本等条件没命中，
            # 通常表示 stale / concurrent update。
            session_b.commit()
        except StaleDataError as exc:
            session_b.rollback()
            print("optimistic concurrency conflict")
            raise ConcurrencyConflictError("A001") from exc
    finally:
        session_a.close()
        session_b.close()


if __name__ == "__main__":
    try:
        main()
    except ConcurrencyConflictError as exc:
        print("business error:", exc)
    session = SessionLocal()
    try:
        row = session.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
        print(f"final quantity={row.quantity} version={row.version_id} (only A's update kept)")
    finally:
        session.close()
    print("\n--- v24 optimistic_lock_demo 运行完毕 ---")
