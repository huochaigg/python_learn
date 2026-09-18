"""Engine、Session factory、get_db。SQLite 文件在 lessons/v20/data/。"""

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from lessons.v20.app.models.base import Base

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

# create_engine(url)：创建 Engine。
# Engine 是连库的核心入口：解析数据库 URL、选择方言/驱动、管理连接池。
# 它本身不是某一条 TCP/SQLite Connection，更像「连接管理器」。
# 真正执行 SQL 时，才会从池里取出 Connection。
# Prisma 对照：没有单独的 Engine 概念，Client 把连接藏得更深。
#
# sqlite:///绝对路径。Path 来自当前文件，不写死某台电脑的盘符（复习 V6）。
#
# connect_args={"check_same_thread": False}：
# SQLite 默认禁止「创建连接的线程」以外的线程使用该连接。
# FastAPI 可能在线程池里跑同步 endpoint，Session 用的连接可能跨线程，
# 所以学习阶段关掉这条检查。这是 SQLite 特有问题，不是 MySQL/PostgreSQL 的常规参数。
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)

# sessionmaker：可配置的 Session 工厂，不是 Session 本身。
# 每次 SessionLocal() 才得到一个新的 Session。
# 全局可以留 factory；不要全局共用一个 Session 给所有请求。
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    # Session：ORM 和数据库交互的主要工作单元。
    # 负责查询、持久化、事务、Identity Map（同一主键尽量对应同一对象）。
    # 需要访问数据库时，才从绑定的 Engine 取 Connection 并开启事务。
    # Session ≠ Connection，也 ≠ Engine。
    # Prisma 对照：使用目的有点像 Prisma Client，生命周期和事务模型并不一样。
    #
    # 每个请求 new 一个 Session，请求结束 close（V18 yield dependency）。
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db() -> None:
    # Base.metadata：所有已加载 Declarative Model 的表结构集合。
    # create_all(bind=engine)：按 metadata 创建还不存在的表，适合 Demo。
    # 它不是 Migration：改列/改约束不会帮你演进旧库。生产用 Alembic。
    # 调用前必须 import User，class 被加载后才会登记进 metadata。
    from lessons.v20.app.models.user import User as _User  # noqa: F401

    Base.metadata.create_all(bind=engine)
