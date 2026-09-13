"""模拟异步数据库 Session。复习 V14 Async Context Manager。"""

import asyncio


class FakeDatabaseSession:
    """假 Session：进入时 connect，退出时 close。不是真正的数据库连接。

    async with 要求对象实现异步 Context Manager 协议：
    await __aenter__() / await __aexit__()。
    普通 open() 或同步对象套上 async with 不会 magically 变成异步 IO。
    """

    def __init__(self, name: str) -> None:
        self.name = name

    async def __aenter__(self) -> "FakeDatabaseSession":
        # 进入 async with 时会被 await。返回值出现在 as 后面。
        print(f"  [db] connect {self.name}")
        await asyncio.sleep(0.02)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        # 离开 async with 时会被 await，异常路径也会走这里（类似 finally）。
        print(f"  [db] close {self.name} exc={exc_type.__name__ if exc_type else None}")
        await asyncio.sleep(0.02)
