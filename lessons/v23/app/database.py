"""独立 SQLite：lessons/v23/data/app.db。不要复用 V22 数据文件。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from lessons.v23.app.models.base import Base

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
    # Session scope vs Transaction scope：
    # FastAPI 一个请求通常 Depends 拿一个 Session。Session 是 ORM 工作环境
    # （对象跟踪、SQL、连接）。Transaction 是其中某一批必须一起成功/失败的
    # 数据库操作。二者不是同一个概念：一个 Session 生命周期里可以有一段
    # 或多段事务，Session close 也不等于某次业务已经 commit。
    #
    # autobegin（默认就有，本课不改 Session 配置）：
    # 第一次真正需要和数据库交互时，Session 通常会自动进入事务。
    # 所以即使没写 session.begin()，CRUD 也不是「完全没有事务」。
    #
    # 谁负责 commit：本课业务事务边界在 Service（with session.begin()）。
    # get_db 只打开/关闭 Session，不在这里替业务拍板。
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    from lessons.v23.app.models.order import Order as _Order  # noqa: F401
    from lessons.v23.app.models.order_item import OrderItem as _OrderItem  # noqa: F401
    from lessons.v23.app.models.stock import Stock as _Stock  # noqa: F401

    Base.metadata.create_all(bind=engine)
