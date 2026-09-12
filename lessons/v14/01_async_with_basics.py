"""V14-01 async with：进入/退出本身也可能要 await。

学习目标：
1. 知道 async with 管的是「异步资源生命周期」。
2. 对象必须自己实现异步 Context Manager 协议。
3. 必须写在 async def 里，普通 def 里不能直接 async with。

运行：uv run python lessons/v14/01_async_with_basics.py
"""

import asyncio


class FakePool:
    """假装建立/关闭都要等网络的连接池。"""

    async def acquire(self) -> str:
        print("  正在建立连接（模拟 IO）")
        await asyncio.sleep(0.05)
        return "conn-1"

    async def release(self, conn: str) -> None:
        print("  正在释放", conn)
        await asyncio.sleep(0.05)


class FakeConnection:
    def __init__(self, pool: FakePool) -> None:
        self.pool = pool
        self.conn: str | None = None

    async def __aenter__(self) -> str:
        self.conn = await self.pool.acquire()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self.conn is not None:
            await self.pool.release(self.conn)


async def main() -> None:
    pool = FakePool()
    # async with：管理「进入和退出本身可能需要异步等待」的资源。
    # 必须由对象实现异步 Context Manager 协议（__aenter__/__aexit__）。
    # 普通 with 调的是同步 __enter__/__exit__，等不了网络。
    # 注意：async with ≠ 把任意同步对象自动变成异步。普通 open() 套上它也不会 magically 变成异步文件 IO。
    print("进入 async with 之前")
    async with FakeConnection(pool) as conn:
        print("as 拿到的资源 =", conn)
        print("在连接里做事")
    print("离开 async with 之后")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 01 async with 运行完毕 ---")

# 本文件重点：
# 1. async with 适合连接、事务、HTTP Client 这类异步资源。
# 2. 进入/退出都可以 await。
# 3. 只能写在 async def 里。
# 4. 对象没实现异步协议，就不能指望 async with 帮你变魔法。
