"""Lost update：两个 Session 都按旧库存计算，后提交的覆盖先提交的。

运行（项目根目录）：
uv run python -m lessons.v24.concurrency_problem_demo

SQLite 的锁行为和 MySQL/PostgreSQL 不同。这里用明确步骤模拟两个请求的
读-改-写。SQLite 只适合学 ORM/事务结构，不要把它的 locking 等同生产库。
"""

from pathlib import Path

from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class DemoBase(DeclarativeBase):
    pass


class PlainStock(DemoBase):
    """Lost Update 必须用不带 version_id_col 的表，否则 ORM 乐观锁会挡住覆盖。"""

    __tablename__ = "plain_stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "lost_update_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def read_qty() -> int:
    session = SessionLocal()
    try:
        return session.execute(select(PlainStock).where(PlainStock.sku == "A001")).scalar_one().quantity
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    DemoBase.metadata.create_all(bind=engine)
    setup = SessionLocal()
    try:
        setup.add(PlainStock(sku="A001", quantity=10))
        setup.commit()
    finally:
        setup.close()

    print("start quantity =", read_qty())
    print("two requests each want to sell 1; theory remaining = 8")

    session_a = SessionLocal()
    session_b = SessionLocal()
    try:
        # 两个独立 Session = 两个并发请求。各自都在事务里，但都先读到 10。
        stock_a = session_a.execute(select(PlainStock).where(PlainStock.sku == "A001")).scalar_one()
        seen_a = stock_a.quantity
        print(f"Session A SELECT quantity={seen_a}")

        stock_b = session_b.execute(select(PlainStock).where(PlainStock.sku == "A001")).scalar_one()
        seen_b = stock_b.quantity
        print(f"Session B SELECT quantity={seen_b}")

        stock_a.quantity = seen_a - 1
        session_a.commit()
        print(f"Session A COMMIT quantity={seen_a - 1} (based on stale snapshot {seen_a})")

        stock_b.quantity = seen_b - 1
        session_b.commit()
        print(f"Session B COMMIT quantity={seen_b - 1} (based on stale snapshot {seen_b})")
    finally:
        session_a.close()
        session_b.close()

    final = read_qty()
    print(f"database quantity={final}; sold in theory=2; remaining should be 8")
    print("transaction existed on both sides, but lost update still happened")
    print("V23 事务保证「一个事务内部多步原子」；挡不住多个事务同时读写同一行。")


if __name__ == "__main__":
    main()
    print("\n--- v24 concurrency_problem_demo 运行完毕 ---")
