"""
文件作用：用 async with session.begin() 验证成功提交和失败回滚。
实际意义：确认 Async Transaction 的 commit/rollback 会真实改动 MySQL 数据。
运行命令：uv run python lessons/v28/03_async_transaction_demo.py
观察重点：事务前数据 / 成功后数据 / 失败后数据；flush 后尚未 commit 也能拿到 order.id。
"""

import asyncio
import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, describe_connect_error, engine
from app.models.order import Order
from app.models.order_item import OrderItem


async def _order_count(session: AsyncSession) -> int:
    return int(await session.scalar(select(func.count()).select_from(Order)) or 0)


async def _has_order(session: AsyncSession, order_no: str) -> bool:
    value = await session.scalar(select(Order.id).where(Order.order_no == order_no))
    return value is not None


async def demo_async_transaction() -> None:
    ok_no = f"OK-{uuid.uuid4().hex[:8]}"
    fail_no = f"FAIL-{uuid.uuid4().hex[:8]}"
    try:
        async with AsyncSessionLocal() as session:
            print(f"事务前 order_count={await _order_count(session)}")

        async with AsyncSessionLocal() as session:
            async with session.begin():
                order = Order(order_no=ok_no, status="pending", total_amount=20)
                session.add(order)
                await session.flush()
                print(f"flush id={order.id}")
                session.add(OrderItem(order_id=order.id, sku="A001", quantity=2, price=10))

        async with AsyncSessionLocal() as session:
            print(f"成功后 order_count={await _order_count(session)}")
            print(f"成功后 has {ok_no}={await _has_order(session, ok_no)}")

        async with AsyncSessionLocal() as session:
            try:
                async with session.begin():
                    order = Order(order_no=fail_no, status="pending", total_amount=9)
                    session.add(order)
                    await session.flush()
                    session.add(OrderItem(order_id=order.id, sku="B001", quantity=1, price=9))
                    raise RuntimeError("business fail")
            except RuntimeError:
                pass

        async with AsyncSessionLocal() as session:
            print(f"失败后 order_count={await _order_count(session)}")
            print(f"失败后 has {fail_no}={await _has_order(session, fail_no)}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        await engine.dispose()


async def main() -> None:
    await demo_async_transaction()


if __name__ == "__main__":
    asyncio.run(main())
