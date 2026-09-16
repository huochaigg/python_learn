"""资源类依赖：yield 模拟 Session / Async Client。"""

import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import Any


class FakeDatabaseSession:
    def query_users(self) -> list[dict[str, Any]]:
        return [{"id": 1, "name": "Ada"}]


def get_session() -> Iterator[FakeDatabaseSession]:
    # yield dependency：
    # - yield 前：创建资源（这里是假 Session）
    # - yield 出去的值：注入 endpoint 的 session
    # - yield 后：清理。必须能在 endpoint 抛错后仍执行，所以用 try/finally。
    # 这和 V14 Async Context Manager / async generator 的「进入-交出-退出」是同一类思路。
    # FastAPI 官方常用这种模式提供 DB Session。这里没有真数据库。
    print("[dep] session open")
    session = FakeDatabaseSession()
    try:
        yield session
    finally:
        print("[dep] session close")


async def get_async_client() -> AsyncIterator[dict[str, str]]:
    print("[dep] async client open")
    await asyncio.sleep(0.02)
    try:
        yield {"name": "fake-http-client"}
    finally:
        await asyncio.sleep(0.02)
        print("[dep] async client close")
