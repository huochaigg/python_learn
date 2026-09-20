"""独立 SQLite：lessons/v24/data/app.db。不要复用 V23 数据文件。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from lessons.v24.app.models.base import Base

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db() -> Iterator[Session]:
    # Session 是请求级 ORM 工作环境；Transaction 是其中一批必须一起成功/失败的操作。
    # 业务事务边界在 Service（session.begin），这里只开关 Session。
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    from lessons.v24.app.models.order import Order as _Order  # noqa: F401
    from lessons.v24.app.models.order_item import OrderItem as _OrderItem  # noqa: F401
    from lessons.v24.app.models.stock import Stock as _Stock  # noqa: F401

    Base.metadata.create_all(bind=engine)
