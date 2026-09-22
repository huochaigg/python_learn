"""
文件作用：用 AsyncSession 查询 users，并演示两个独立 Session + gather。
实际意义：看 AsyncSession 和 AsyncEngine 如何协作；并发任务应各自使用独立 Session。
运行命令：uv run python lessons/v28/02_async_session_demo.py
观察重点：查询结果、session_a is session_b 为 False、两个 Task 各自 Session 都能查到数据。
"""

import asyncio

from sqlalchemy import select

from app.database import AsyncSessionLocal, describe_connect_error, engine
from app.models.user import User


async def _query_users(session, label: str) -> None:
    stmt = select(User).order_by(User.id.asc())
    result = await session.execute(stmt)
    rows = list(result.scalars().all())
    print(f"{label} user_count={len(rows)}")
    for row in rows:
        print(f"{label} id={row.id} name={row.name} email={row.email}")


async def demo_async_session() -> None:
    try:
        async with AsyncSessionLocal() as session:
            await _query_users(session, "single")

        async with AsyncSessionLocal() as session_a, AsyncSessionLocal() as session_b:
            print(f"session_a is session_b = {session_a is session_b}")
            # 这只是演示「每个并发任务各自 Session」，并不意味着真实业务
            # 应该随意把所有 SQL gather 并发执行。事务边界和连接池压力需要额外考虑。
            await asyncio.gather(
                _query_users(session_a, "A"),
                _query_users(session_b, "B"),
            )
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        await engine.dispose()


async def main() -> None:
    await demo_async_session()


if __name__ == "__main__":
    asyncio.run(main())
