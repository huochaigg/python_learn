"""
文件作用：创建 python_learn_v30 的 products 表并幂等写入测试库存。
实际意义：流式库存查询仍然走真实 MySQL，必须先有表和 SKU001/002/003。
运行命令：uv run python lessons/v30/init_db.py
观察重点：打印 database 和 products 行，重复运行不会再插入重复 SKU。
"""

import asyncio

from sqlalchemy import func, select, text

from app.core.database import AsyncSessionLocal, engine, init_schema, seed_products
from app.models.product import Product


async def main() -> None:
    await init_schema()
    await seed_products()
    async with engine.connect() as connection:
        database = (await connection.execute(text("SELECT DATABASE()"))).scalar()
    async with AsyncSessionLocal() as session:
        count = int(await session.scalar(select(func.count()).select_from(Product)) or 0)
        rows = list((await session.execute(select(Product).order_by(Product.sku))).scalars())
    print(f"database={database}")
    print(f"product_count={count}")
    for row in rows:
        print(f"{row.sku} {row.name} stock={row.stock}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
