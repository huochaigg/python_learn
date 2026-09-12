"""V14-04 async for：下一项可能需要等待。

学习目标：
1. list 能 for，但不能因此就能 async for。
2. Async Generator 要用 async for 消费。
3. async for 必须写在 async def 里。

运行：uv run python lessons/v14/04_async_for_basics.py
"""

import asyncio


def sync_items() -> list[str]:
    return ["a", "b", "c"]


async def stream_items():
    for item in ["a", "b", "c"]:
        await asyncio.sleep(0.05)
        yield item


async def main() -> None:
    print("普通 list 用 for：数据已经在内存里")
    for x in sync_items():
        print(" ", x)

    # list 不是 Async Iterable。写在 async def 里也不会自动变。
    # 不要为了「看起来异步」把已经在内存的 list 硬包成复杂 Async Iterator。
    try:
        async for x in sync_items():  # type: ignore[attr-defined]
            print(" ", x)
    except TypeError as e:
        print("list 不能 async for：", e)

    print("\nAsync Generator 用 async for：每次下一项都可能 await")
    # async for：消费 Async Iterable。
    # 每次取下一项都可能等待（网络消息、DB 流、AI token）。
    # 简化模型：__aiter__() → 反复 await __anext__() → StopAsyncIteration。
    async for x in stream_items():
        print(" ", x)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 04 async for 运行完毕 ---")

# 本文件重点：
# 1. for 走同步 Iterator；async for 走异步 Iterator。
# 2. 普通 list 不能直接 async for。
# 3. 异步流才值得 async for，内存里的小 list 用普通 for。
# 4. async for 只能出现在 async def 中。
