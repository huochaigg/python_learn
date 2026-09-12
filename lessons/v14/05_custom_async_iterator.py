"""V14-05 手写 Async Iterator：__aiter__ / __anext__ / StopAsyncIteration。

学习目标：
1. 对照同步 __iter__/__next__/StopIteration。
2. 每次取下一项都可以 await。
3. 用 async for 消费，看到它会自动处理 StopAsyncIteration。

运行：uv run python lessons/v14/05_custom_async_iterator.py
"""

import asyncio


class AsyncCounter:
    def __init__(self, max_value: int) -> None:
        self.max_value = max_value
        self.current = 0

    def __aiter__(self) -> "AsyncCounter":
        # __aiter__()：返回 Async Iterator。这里返回 self。
        # 对比同步 __iter__()。
        return self

    async def __anext__(self) -> int:
        # __anext__()：异步取下一个元素，可以 await。
        # 对比同步 __next__()。没有下一项时 raise StopAsyncIteration。
        # 对比同步的 StopIteration。
        if self.current >= self.max_value:
            raise StopAsyncIteration
        self.current += 1
        await asyncio.sleep(0.2)
        return self.current


async def main() -> None:
    print("async for 会自动 await __anext__，并处理 StopAsyncIteration:")
    async for n in AsyncCounter(3):
        print(" ", n)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 05 自定义 Async Iterator 运行完毕 ---")

# 本文件重点：
# 1. __aiter__ + async __anext__ = Async Iterator。
# 2. 结束信号是 StopAsyncIteration，不是 StopIteration。
# 3. 下一项可等待，适合网络流，不适合已经在内存的 list。
# 4. 日常更常用 Async Generator，手写 class 是为了看清协议。
