"""
文件作用：创建 python_learn_v31 的商品表、业务会话表，并幂等写入测试库存。
实际意义：Session 历史和库存 Tool 都走真实 MySQL，启动前必须有库和 SKU。
运行命令：uv run python lessons/v31/init_db.py
观察重点：database=python_learn_v31；products 三行；conversations/messages 表可查询。
"""

import asyncio

from sqlalchemy import func, select, text

from app.core.database import AsyncSessionLocal, engine, init_schema, seed_products
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.product import Product
from app.sessions.agent_session import init_sdk_session_tables


async def main() -> None:
    await init_schema()
    await seed_products()
    await init_sdk_session_tables()
    async with engine.connect() as connection:
        database = (await connection.execute(text("SELECT DATABASE()"))).scalar()
        tables = [
            row[0]
            for row in (
                await connection.execute(
                    text(
                        "SELECT table_name FROM information_schema.tables "
                        "WHERE table_schema = DATABASE() ORDER BY table_name"
                    )
                )
            ).all()
        ]
    async with AsyncSessionLocal() as session:
        product_count = int(await session.scalar(select(func.count()).select_from(Product)) or 0)
        conversation_count = int(
            await session.scalar(select(func.count()).select_from(Conversation)) or 0
        )
        message_count = int(await session.scalar(select(func.count()).select_from(Message)) or 0)
        rows = list((await session.execute(select(Product).order_by(Product.sku))).scalars())
    print(f"database={database}")
    print(f"tables={tables}")
    print(f"product_count={product_count}")
    print(f"conversation_count={conversation_count}")
    print(f"message_count={message_count}")
    for row in rows:
        print(f"{row.sku} {row.name} stock={row.stock}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
