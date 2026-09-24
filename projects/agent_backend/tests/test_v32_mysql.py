import os

import pytest
from sqlalchemy import select

from app.core.config import settings
from app.core.database import AsyncSessionLocal, engine, init_schema, migrate_schema, seed_products
from app.models.product import Product
from app.repositories.product_repository import product_repository


pytestmark = pytest.mark.asyncio


async def test_mysql_product_stock_sku002() -> None:
    if not settings.database_password and not os.getenv("DATABASE_PASSWORD"):
        pytest.skip("MySQL 未配置")
    await init_schema()
    await migrate_schema()
    await seed_products()
    async with AsyncSessionLocal() as session:
        product = await product_repository.get_by_sku(session, "SKU002")
        assert product is not None
        assert product.stock == 8
        missing = await product_repository.get_by_sku(session, "SKU999")
        assert missing is None
        count = len(list((await session.execute(select(Product))).scalars()))
        assert count >= 3
    await engine.dispose()
