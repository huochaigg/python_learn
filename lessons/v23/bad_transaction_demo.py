"""错误示范：中间 commit 后再失败。第一步会留下。

运行（项目根目录）：
uv run python -m lessons.v23.bad_transaction_demo

结论：一个完整业务若要「全部成功或全部失败」，不要在中间随意 commit。
rollback 只能撤销当前尚未 commit 的事务。
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from lessons.v23.app.models.base import Base
from lessons.v23.app.models.stock import Stock

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "bad_transaction_demo.db"
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


def wrongly_commit_in_the_middle() -> None:
    session = SessionLocal()
    try:
        a = session.execute(select(Stock).where(Stock.sku == "A001")).scalar_one()
        a.quantity -= 1
        session.commit()
        print("WRONG: step1 already committed A001 -= 1")

        b = session.execute(select(Stock).where(Stock.sku == "B001")).scalar_one()
        b.quantity -= 1
        raise RuntimeError("step2 failed after step1 commit")
        session.commit()
    except Exception:
        # 这里的 rollback 只能撤销「当前」还没 commit 的事务（step2）。
        # step1 已经 commit，无法被这次 rollback 撤回。
        session.rollback()
        raise
    finally:
        session.close()


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    seed_demo()
    snapshot("before")
    try:
        wrongly_commit_in_the_middle()
    except RuntimeError as exc:
        print("caller caught:", exc)
    snapshot("after (A001 is 9 forever; B001 still 20)")
    print("lesson: do not commit in the middle of one business action")


if __name__ == "__main__":
    main()
    print("\n--- v23 bad_transaction_demo 运行完毕 ---")
