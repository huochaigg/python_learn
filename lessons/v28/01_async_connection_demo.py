"""
文件作用：直接通过 AsyncEngine 连接 MySQL
实际意义：确认 asyncmy + SQLAlchemy AsyncEngine + MySQL 真正连通
运行命令：uv run python lessons/v28/01_async_connection_demo.py
观察重点：真实 MySQL version/database/SELECT 结果是否通过 await 获取
"""

import asyncio

from sqlalchemy import text

from app.database import describe_connect_error, engine


async def demo_async_connection() -> None:
    try:
        # async with engine.connect()：进入时异步 checkout Connection；
        # 退出时释放/归还连接资源，不是关闭整个 AsyncEngine。
        async with engine.connect() as connection:
            version = (await connection.execute(text("SELECT VERSION()"))).scalar()
            database = (await connection.execute(text("SELECT DATABASE()"))).scalar()
            one = (await connection.execute(text("SELECT 1"))).scalar()
            print(f"MySQL version={version}")
            print(f"database={database}")
            print(f"SELECT 1={one}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        # dispose()：释放整个 Engine 的连接池资源，适合脚本/应用关闭阶段。
        # 绝对不要每个 FastAPI request dispose engine。
        await engine.dispose()


async def main() -> None:
    await demo_async_connection()


if __name__ == "__main__":
    asyncio.run(main())
