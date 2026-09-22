"""应用级 AsyncEngine / Pool / AsyncSession。单个进程里长期复用 Engine。"""

from collections.abc import AsyncIterator

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

# create_async_engine()：创建 SQLAlchemy AsyncEngine，配合 asyncio-compatible dialect。
# 角色与同步 Engine 类似，仍然管理数据库连接和连接池，但 Connection 获取 / 数据库 IO 通过 await 驱动。
# 在单个应用进程里创建一次、长期复用。Request 级应该创建 AsyncSession，而不是 Engine。
engine = create_async_engine(
    settings.database_url,
    # 含义见 V27，同样作用于当前 AsyncEngine 对应 Pool。
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
)

# async_sessionmaker：AsyncSession factory，不是某一个 Session；每次调用才创建新的 AsyncSession。
# expire_on_commit=False：commit 后 ORM object 默认可能被 expire，随后访问属性可能需要重新加载。
# async 场景应尽量避免这种隐式 IO，因此官方 asyncio 示例经常使用 False。
# 不是「异步必须永远 False」，只是当前学习项目按官方示例这样选。
#
# AsyncSession：同步 Session 的 asyncio 代理 / 异步接口，仍然是有状态的 transaction/session object。
# 不能因为名字带 async 就把它共享给多个并发 asyncio Task。
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncIterator[AsyncSession]:
    # async with 管理 AsyncSession 生命周期；yield 把 Session 注入 FastAPI endpoint；
    # dependency 结束后 context manager 自动 close。
    async with AsyncSessionLocal() as session:
        yield session


async def init_schema() -> None:
    from .models import Base
    from .models.order import Order as _Order  # noqa: F401
    from .models.order_item import OrderItem as _OrderItem  # noqa: F401
    from .models.user import User as _User  # noqa: F401

    async with engine.begin() as conn:
        # Metadata.create_all 是同步 SQLAlchemy API。
        # AsyncConnection.run_sync() 允许它在 AsyncEngine Connection 上正确执行。
        await conn.run_sync(Base.metadata.create_all)


def describe_connect_error(exc: BaseException) -> str:
    if isinstance(exc, ModuleNotFoundError) and "asyncmy" in str(exc).lower():
        return "driver 未安装 (asyncmy)"
    if isinstance(exc, ModuleNotFoundError) and "greenlet" in str(exc).lower():
        return "缺少 greenlet（SQLAlchemy asyncio 依赖）"

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


async def check_db_health(session: AsyncSession) -> dict[str, object]:
    value = (await session.execute(text("SELECT 1"))).scalar()
    return {
        "status": "ok" if value == 1 else "error",
        "database": "mysql",
        "db_name": settings.db_name,
        "select_1": value,
    }


async def list_tables() -> list[str]:
    async with engine.connect() as conn:
        return await conn.run_sync(lambda sync_conn: list(inspect(sync_conn).get_table_names()))
