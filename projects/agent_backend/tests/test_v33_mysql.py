import os

import pytest
from sqlalchemy import select

from app.core.config import settings
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)
from app.models.order import Order
from app.repositories.order_repository import order_repository
from app.repositories.product_repository import product_repository


pytestmark = pytest.mark.asyncio


def _has_mysql() -> bool:
    return bool(settings.database_password or os.getenv("DATABASE_PASSWORD"))


async def test_order_seed_and_ownership() -> None:
    if not _has_mysql():
        pytest.skip("MySQL 未配置")
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    async with AsyncSessionLocal() as session:
        product = await product_repository.get_by_sku(session, "SKU002")
        assert product is not None
        assert product.stock == 8
        order = await order_repository.get_by_order_no(session, "ORD001")
        assert order is not None
        assert order.status == "shipped"
        assert order.user_id == 1
        owned = await order_repository.get_owned(session, "ORD001", 1)
        assert owned is not None
        foreign = await order_repository.get_owned(session, "ORD003", 1)
        assert foreign is None
        missing = await order_repository.get_by_order_no(session, "ORD999")
        assert missing is None
        count = len(list((await session.execute(select(Order))).scalars()))
        assert count >= 3
    await engine.dispose()
