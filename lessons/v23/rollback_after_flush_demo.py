"""flush 撞上 unique 约束后，必须 rollback 才能继续用这个 Session。

运行（项目根目录）：
uv run python -m lessons.v23.rollback_after_flush_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from lessons.v23.app.exceptions.business import DuplicateOrderNoError
from lessons.v23.app.models.base import Base
from lessons.v23.app.models.order import Order

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "rollback_after_flush_demo.db"
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.add(Order(order_no="DUP-1", status="pending", total_amount=1))
        session.commit()
        print("first order committed")

        try:
            session.add(Order(order_no="DUP-1", status="pending", total_amount=2))
            # flush 失败会让当前 Session transaction 进入失败状态。
            # 调用方应该 rollback，或丢弃/关闭这个 Session 后再继续。
            # 官方要求：flush 失败后应用执行 rollback 来恢复 Session。
            # 不要 except Exception: rollback; return None。rollback 后继续 raise，
            # 或转成明确业务异常 raise ... from e。
            session.flush()
            session.commit()
        except IntegrityError as exc:
            session.rollback()
            raise DuplicateOrderNoError("DUP-1") from exc
    finally:
        session.close()


if __name__ == "__main__":
    try:
        main()
    except DuplicateOrderNoError as exc:
        print("business error after rollback+raise:", exc)

    session = SessionLocal()
    try:
        nos = [row.order_no for row in session.execute(select(Order)).scalars()]
        print("orders left =", nos, "(only the first committed DUP-1)")
    finally:
        session.close()
    print("\n--- v23 rollback_after_flush_demo 运行完毕 ---")
