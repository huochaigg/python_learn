"""
文件作用：使用 AsyncEngine 创建 V28 MySQL 表
实际意义：学习 async connection 如何执行同步 metadata DDL API
运行命令：uv run python lessons/v28/init_db.py
观察重点：MySQL 是否真实创建 users/orders/order_items 表
"""

import asyncio

from sqlalchemy import text

from app.database import describe_connect_error, engine, init_schema, list_tables


async def main() -> None:
    try:
        await init_schema()
        async with engine.connect() as connection:
            database = (await connection.execute(text("SELECT DATABASE()"))).scalar()
        print(f"database={database}")
        print(f"tables={sorted(await list_tables())}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
