"""应用级 AsyncEngine。Request 级创建 AsyncSession，不要把 Session 绑到全局 Agent。"""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_timeout=settings.db_pool_timeout,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    # Request-scoped Session：整个 Runner.run() 必须在这个 yield 期间完成。
    # Agent 是模块级配置，可以复用；AsyncSession 不能放进 Agent 实例，也不能给多个并发 Task 共用。
    async with AsyncSessionLocal() as session:
        yield session


async def init_schema() -> None:
    from ..models import Base
    from ..models.product import Product as _Product  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_products() -> None:
    from ..models.product import Product
    from ..repositories.product_repository import product_repository

    initial = [
        ("SKU001", "机械键盘", 100),
        ("SKU002", "显示器", 8),
        ("SKU003", "显卡", 0),
    ]
    async with AsyncSessionLocal() as session:
        for sku, name, stock in initial:
            if await product_repository.get_by_sku(session, sku) is None:
                session.add(Product(sku=sku, name=name, stock=stock))
        await session.commit()
