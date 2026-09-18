"""独立 SQLite：lessons/v21/data/app.db。不要复用 V20 数据文件。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lessons.v21.app.models.base import Base

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

# echo 默认关闭。echo=True 会把 SQL/参数打到终端，学习和调试方便，
# 但生产应走 logging 配置，不建议正式默认一直开。教学演示见 query_demo.py。
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    from lessons.v21.app.models.user import User as _User  # noqa: F401

    Base.metadata.create_all(bind=engine)
