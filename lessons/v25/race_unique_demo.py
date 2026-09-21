"""
文件作用：用两个 Session 说明「先查 email 不存在」挡不住并发重复插入。
重点概念：应用层先查不是并发安全；UNIQUE 才是最终防线。
观察重点：A/B 都查到不存在后，只有一个 INSERT 成功，另一个 IntegrityError。
"""

from pathlib import Path

from sqlalchemy import create_engine, event, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from lessons.v25.app.models.base import Base
from lessons.v25.app.models.user import User

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "race_unique_demo.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def email_exists(session, email: str) -> bool:
    return (
        session.execute(select(User).where(User.email == email)).scalar_one_or_none()
        is not None
    )


def main() -> None:
    DB_PATH.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    session_a = SessionLocal()
    session_b = SessionLocal()
    try:
        print("A checks exists?", email_exists(session_a, "race@example.com"))
        print("B checks exists?", email_exists(session_b, "race@example.com"))
        print("both think they can insert")

        session_a.add(User(name="A", email="race@example.com"))
        session_a.commit()
        print("A insert committed")

        session_b.add(User(name="B", email="race@example.com"))
        try:
            session_b.commit()
        except IntegrityError as extra:
            session_b.rollback()
            print("B insert blocked by UNIQUE:", type(extra).__name__)
    finally:
        session_a.close()
        session_b.close()

    session = SessionLocal()
    try:
        rows = list(session.execute(select(User)).scalars())
        print("users left:", [(row.name, row.email) for row in rows])
    finally:
        session.close()


if __name__ == "__main__":
    main()
    print("\n--- v25 race_unique_demo 运行完毕 ---")
