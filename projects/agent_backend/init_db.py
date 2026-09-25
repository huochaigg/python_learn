"""
文件作用：创建 python_learn_agent 的商品表、订单表、会话表，并补齐 message_type 列。
实际意义：长期项目独立数据库，库存 Tool、订单 Tool 和 Session 历史都走真实 MySQL。
运行命令：uv run python projects/agent_backend/init_db.py
观察重点：database=python_learn_agent；products 三行；orders 三行；messages 含 message_type。
"""

import asyncio

from sqlalchemy import func, select, text

from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.order import Order
from app.models.product import Product
from app.sessions.agent_session import init_sdk_session_tables


async def main() -> None:
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
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
        order_count = int(await session.scalar(select(func.count()).select_from(Order)) or 0)
        conversation_count = int(
            await session.scalar(select(func.count()).select_from(Conversation)) or 0
        )
        message_count = int(await session.scalar(select(func.count()).select_from(Message)) or 0)
        products = list((await session.execute(select(Product).order_by(Product.sku))).scalars())
        orders = list((await session.execute(select(Order).order_by(Order.order_no))).scalars())
    print(f"database={database}")
    print(f"tables={tables}")
    print(f"product_count={product_count}")
    print(f"order_count={order_count}")
    print(f"conversation_count={conversation_count}")
    print(f"message_count={message_count}")
    for row in products:
        print(f"{row.sku} {row.name} stock={row.stock}")
    for row in orders:
        print(f"{row.order_no} user={row.user_id} sku={row.sku} status={row.status}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
