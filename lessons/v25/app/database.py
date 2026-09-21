"""独立 SQLite：lessons/v25/data/app.db。不要复用 V24 数据文件。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from lessons.v25.app.models.base import Base

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
    # event.listens_for(engine, "connect")：每次从这个 Engine 拿出一条底层连接时回调。
    # 用来给该连接做一次性设置，而不是改 SQLAlchemy 查询 API。
    #
    # SQLite 默认不强制 FOREIGN KEY（和其他库不一样）。
    # 必须 PRAGMA foreign_keys=ON，本课的 FK Demo 才会真正失败。
    # 不要以为 MySQL/PostgreSQL 也要写这条 PRAGMA。
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    from lessons.v25.app.models.order import Order as _Order  # noqa: F401
    from lessons.v25.app.models.order_item import OrderItem as _OrderItem  # noqa: F401
    from lessons.v25.app.models.stock import Stock as _Stock  # noqa: F401
    from lessons.v25.app.models.user import User as _User  # noqa: F401

    Base.metadata.create_all(bind=engine)
