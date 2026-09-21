"""
文件作用：演示 IntegrityError 之后必须 rollback，Session 才能继续用。
重点概念：sqlalchemy.exc.IntegrityError、flush/commit 失败后的事务状态、V23 rollback。
观察重点：正确流程 rollback 后还能查询；错误流程不 rollback 时后续操作失败。
"""

from pathlib import Path

from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.orm import sessionmaker

from lessons.v25.app.models.base import Base
from lessons.v25.app.models.user import User

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "integrity_error_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def demo_integrity_error_flow() -> None:
    print("\n===== demo_integrity_error_flow =====")
    session = SessionLocal()
    try:
        session.add(User(name="Ada", email="ada@example.com"))
        session.commit()
        session.add(User(name="Bob", email="ada@example.com"))
        try:
            # IntegrityError：数据库完整性约束失败对应的 SQLAlchemy 异常。
            # 常见来源：UNIQUE / NOT NULL / CHECK / ForeignKey。
            # 它是失败信号，不是用户友好的业务异常，不要 str(e) 回给前端。
            session.flush()
        except IntegrityError as extra:
            print("caught", type(extra).__name__)
            # 关联 V23：flush/commit 失败后事务进入失败状态，必须 rollback。
            session.rollback()
            print("rolled back; session usable again")
            n = session.scalar(select(User.email).where(User.email == "ada@example.com"))
            print("still only one ada:", n)
    finally:
        session.close()


def demo_forgot_rollback() -> None:
    print("\n===== demo_forgot_rollback (wrong) =====")
    session = SessionLocal()
    try:
        session.add(User(name="Eve", email="eve@example.com"))
        session.commit()
        session.add(User(name="Eve2", email="eve@example.com"))
        try:
            session.flush()
        except IntegrityError:
            print("caught IntegrityError but NOT rolling back")
        try:
            session.execute(select(User)).scalars().all()
            print("unexpected: query succeeded")
        except PendingRollbackError as extra:
            print("subsequent use failed:", type(extra).__name__)
        session.rollback()
        print("after explicit rollback, query works:", len(list(session.execute(select(User)).scalars())))
    finally:
        session.close()


# 个人测试
def demo_personal_test() -> None:
    print("\n===== demo_personal_test =====")
    session = SessionLocal()
    try:
        result = session.execute(select(User))
        scalars = result.scalars()
        all_users = scalars.all()
        print("个人测试数据：")
        print('result', result)
        print('scalars', scalars)
        print('all_users', all_users)

        for user in all_users:
            print(user, user.name, user.email)
    finally:
        session.close()

def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    demo_integrity_error_flow()
    demo_forgot_rollback()
    demo_personal_test()


if __name__ == "__main__":
    main()
    print("\n--- v25 integrity_error_demo 运行完毕 ---")
