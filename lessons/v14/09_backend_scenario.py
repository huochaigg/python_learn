"""V14-09 后端组合：async with 管连接，async for 读流。

学习目标：
1. 资源生命周期 + 异步数据流怎么叠在一起。
2. 读到一半抛错时，close 仍然执行。
3. 通过 print 看 connect → read → error → close。

运行：uv run python lessons/v14/09_backend_scenario.py
"""

import asyncio


class AsyncOrderClient:
    def __init__(self) -> None:
        self.closed = False

    async def __aenter__(self) -> "AsyncOrderClient":
        print("connect")
        await asyncio.sleep(0.05)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        print("close", "because", exc_type.__name__ if exc_type else "normal")
        await asyncio.sleep(0.05)
        self.closed = True

    async def orders(self):
        rows = ["o-1", "o-2", "BAD", "o-4"]
        for row in rows:
            await asyncio.sleep(0.05)
            print("read", row)
            if row == "BAD":
                raise ValueError("corrupt row")
            yield row


async def main() -> None:
    try:
        async with AsyncOrderClient() as client:
            async for order_id in client.orders():
                print("handle", order_id)
    except ValueError as e:
        print("error", e)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 09 后端场景 运行完毕 ---")

# 本文件重点：
# 1. async with 管连接；async for 消费这个连接上的流。
# 2. 内部可以用 Async Generator 模拟数据源。
# 3. 中途异常也会 close，顺序应是 connect → read → error → close。
# 4. 以后 SQLAlchemy Session / HTTP client 就是这个形状。
