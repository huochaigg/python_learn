"""
文件作用：用 selectinload 查询 Order + items，输出真实 order_no 和 sku 列表。
实际意义：演示 AsyncSession 下应明确加载 relationship，避免普通属性访问产生隐式 IO。
运行命令：uv run python lessons/v28/04_async_relationship_demo.py
观察重点：订单号和 item sku 是否一次查询就能打印出来。不要用会崩溃的 lazy load 当主路径。
"""

import asyncio
import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import AsyncSessionLocal, describe_connect_error, engine
from app.models.order import Order
from app.models.order_item import OrderItem


async def demo_async_relationship() -> None:
    order_no = f"REL-{uuid.uuid4().hex[:8]}"
    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                order = Order(order_no=order_no, status="pending", total_amount=30)
                session.add(order)
                await session.flush()
                session.add(OrderItem(order_id=order.id, sku="A001", quantity=1, price=10))
                session.add(OrderItem(order_id=order.id, sku="B001", quantity=2, price=10))

        async with AsyncSessionLocal() as session:
            stmt = select(Order).options(selectinload(Order.items)).where(Order.order_no == order_no)
            loaded = (await session.execute(stmt)).scalar_one()
            skus = [item.sku for item in loaded.items]
            print(f"order_no={loaded.order_no}")
            print(f"item_count={len(skus)}")
            print(f"skus={skus}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        await engine.dispose()


async def main() -> None:
    await demo_async_relationship()


if __name__ == "__main__":
    asyncio.run(main())
