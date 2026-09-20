"""悲观锁 API：with_for_update() → SELECT ... FOR UPDATE。

运行（项目根目录）：
uv run python -m lessons.v24.pessimistic_lock_demo

SQLite 不完整支持生产库的行锁语义。本文件只学 SQLAlchemy API 和事务流程，
不要得出「SQLite 已经完整证明 FOR UPDATE 工作」的结论。
真正并发等待以后换 MySQL/PostgreSQL 再验证。
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from lessons.v24.app.models.base import Base
from lessons.v24.app.models.stock import Stock

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "pessimistic_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def show_sql() -> None:
    sku = "A001"
    # with_for_update()：在支持的数据库上生成 SELECT ... FOR UPDATE。
    # 事务期间锁定选中行，直到 commit/rollback 才释放。
    # 锁的是数据库资源，不是 Python threading.Lock。
    stmt = select(Stock).where(Stock.sku == sku).with_for_update()
    print("\n===== with_for_update() =====")
    print(stmt)

    # nowait=True：拿不到锁时尝试立即失败（不要一直等）。不是所有 backend 都一样。
    # 不要用在本课正式库存逻辑里。
    stmt_nowait = select(Stock).where(Stock.sku == sku).with_for_update(nowait=True)
    print("\n===== with_for_update(nowait=True) =====")
    print(stmt_nowait)

    # skip_locked=True：跳过已经被其他事务锁住的行。更常见于多 Worker 抢任务。
    # 不同数据库支持不同，不能认为所有 backend 行为一样。
    stmt_skip = select(Stock).where(Stock.sku == sku).with_for_update(skip_locked=True)
    print("sqlite dialect may compile nowait/skip_locked as plain FOR UPDATE;")
    print("do not treat these three prints as proof that sqlite implements all options.")


def theoretical_flow() -> None:
    print(
        """
===== theoretical flow (MySQL/PostgreSQL row lock) =====
Transaction A: BEGIN
Transaction A: SELECT * FROM stocks WHERE sku='A001' FOR UPDATE   -- A holds the row
Transaction A: check quantity, quantity = quantity - 1
Transaction A: COMMIT   -- lock released
Transaction B: was waiting; now can SELECT ... FOR UPDATE and continue

事务必须短。禁止持有 FOR UPDATE 时去 sleep 或调用外部支付。
如果 Demo 用 sleep 展示等待，那只是教学，生产不要持锁做慢 IO。
本课不 sleep。
"""
    )


def run_api_on_sqlite() -> None:
    print("===== sqlite execute (API practice only, not a row-lock proof) =====")
    session = SessionLocal()
    try:
        with session.begin():
            stmt = select(Stock).where(Stock.sku == "A001").with_for_update()
            stock = session.execute(stmt).scalar_one()
            print("locked row (sqlite may ignore real row lock):", stock.sku, stock.quantity)
            if stock.quantity >= 1:
                stock.quantity -= 1
        print("after commit quantity =", read_qty())
    finally:
        session.close()


def read_qty() -> int:
    session = SessionLocal()
    try:
        return session.execute(select(Stock).where(Stock.sku == "A001")).scalar_one().quantity
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add(Stock(sku="A001", quantity=10, version_id=1))
        session.commit()
    finally:
        session.close()
    show_sql()
    theoretical_flow()
    run_api_on_sqlite()


if __name__ == "__main__":
    main()
    print("\n--- v24 pessimistic_lock_demo 运行完毕 ---")
