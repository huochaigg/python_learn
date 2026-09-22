"""应用级 MySQL Engine / Pool / Session。单个进程里长期复用 Engine。"""

from collections.abc import Iterator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

# create_engine()：在单个应用进程里创建一次、长期复用。
# Engine 管理连接池里的多条底层连接，不应该每个 HTTP Request 都重新 create_engine。
engine = create_engine(
    settings.database_url,
    # pool_size：连接池长期维护的基础连接数量。
    # 它不代表 FastAPI 只能同时处理这么多个 HTTP Request。
    pool_size=settings.db_pool_size,
    # max_overflow：基础连接都被 checkout 时，还可以额外创建的临时连接数量。
    # 不要把它理解成「数据库最大连接数」。
    max_overflow=settings.db_max_overflow,
    # pool_timeout：池里暂时没有可用连接时，调用方最多等待多少秒。
    # 超时常见报错是 QueuePool timeout（连接池耗尽），不是 MySQL 本身宕机。
    pool_timeout=settings.db_pool_timeout,
    # pool_recycle：连接存活超过该秒数后，下次 checkout 时回收/重建。
    # 用来应对 MySQL 长连接超时；不是「每 N 秒主动重启整个连接池」。
    pool_recycle=settings.db_pool_recycle,
    # pool_pre_ping=True：从池中取出 Connection 时先验证是否仍可用。
    # 主要处理池里 stale/disconnected connection；不是每条 SQL 都 ping，也不是业务健康检查。
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine)


def get_db() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        # Session.close() 结束 ORM Session 生命周期。
        # 底层 DBAPI Connection 通常被归还 Engine 的连接池，而不是每次永久断开 MySQL TCP。
        session.close()


def init_schema() -> None:
    # create_all 只是学习初始化，用来在空库上建表。正式 schema 变更应使用 Alembic，不是本课内容。
    from .models.user import User as _User  # noqa: F401
    from .models import Base

    Base.metadata.create_all(bind=engine)


def describe_connect_error(exc: BaseException) -> str:
    if isinstance(exc, ModuleNotFoundError) and "pymysql" in str(exc).lower():
        return "driver 未安装 (PyMySQL)"

    orig = getattr(exc, "orig", exc)
    code = orig.args[0] if getattr(orig, "args", None) else None
    labels = {
        2002: "host/port 不通",
        2003: "host/port 不通",
        1044: "access denied",
        1045: "access denied",
        1049: "database 不存在",
    }
    if isinstance(code, int) and code in labels:
        return f"{labels[code]} ({type(exc).__name__})"
    return f"其他错误 ({type(exc).__name__}: {exc})"


def check_db_health(session: Session) -> dict[str, object]:
    # text()：显式构造 textual SQL。这里只用于简单健康检查；业务 ORM 查询仍优先使用 select(Model)。
    value = session.execute(text("SELECT 1")).scalar()
    return {
        "status": "ok" if value == 1 else "error",
        "database": "mysql",
        "db_name": settings.db_name,
        "select_1": value,
    }


def list_tables() -> list[str]:
    return list(inspect(engine).get_table_names())
