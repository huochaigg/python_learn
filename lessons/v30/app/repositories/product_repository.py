from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.product import Product


class ProductRepository:
    async def get_by_sku(self, session: AsyncSession, sku: str) -> Product | None:
        stmt = select(Product).where(Product.sku == sku)
        return (await session.execute(stmt)).scalar_one_or_none()


product_repository = ProductRepository()
