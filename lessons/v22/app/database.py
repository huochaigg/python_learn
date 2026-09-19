"""独立 SQLite：lessons/v22/data/app.db。不要复用 V21 数据文件。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from lessons.v22.app.models.base import Base

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

# echo 默认关闭。教学 SQL 日志在 relationship_demo / n_plus_one_demo 里打开。
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    # SQLite 默认不强制 FOREIGN KEY。打开后 ForeignKey 约束才会真正生效。
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    from lessons.v22.app.models.order import Order as _Order  # noqa: F401
    from lessons.v22.app.models.order_item import OrderItem as _OrderItem  # noqa: F401

    Base.metadata.create_all(bind=engine)
