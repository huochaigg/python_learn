"""V14-06 Async Generator：async def + yield。

学习目标：
1. 对照同步 def + yield。
2. 分清：async def + return → Coroutine；async def + yield → Async Generator。
3. 调用生成器函数不会立刻跑完全部。

运行：uv run python lessons/v14/06_async_generator.py
"""

import asyncio
import inspect


def sync_count():
    yield 1
    yield 2


async def fetch_user() -> str:
    """只有 return：Coroutine Function。"""
    await asyncio.sleep(0.02)
    return "Ada"


async def stream_numbers():
    # async def + yield = Async Generator Function。
    # 调用后得到 Async Generator Object，不是 Coroutine，也不能直接 await 完整个流。
    # 通常用 async for 或 anext() 消费。
    print("  还没到第一个 yield")
    await asyncio.sleep(0.05)
    yield 1
    await asyncio.sleep(0.05)
    yield 2
    await asyncio.sleep(0.05)
    yield 3


async def main() -> None:
    print("同步 generator type =", type(sync_count()))
    print("fetch_user 是 coroutine function?", inspect.iscoroutinefunction(fetch_user))
    print("stream_numbers 是 async generator function?", inspect.isasyncgenfunction(stream_numbers))

    coro = fetch_user()
    print("async def + return 的调用 type =", type(coro))
    print("  iscoroutine?", inspect.iscoroutine(coro))
    print("  await coroutine =", await coro)

    agen = stream_numbers()
    print("async def + yield 的调用 type =", type(agen))
    print("  isasyncgen?", inspect.isasyncgen(agen))
    print("注意：创建 agen 时几乎还没执行函数体；也不能直接 await agen")
    print("用 async for 推动它：")
    async for n in agen:
        print(" ", n)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 06 Async Generator 运行完毕 ---")

# 本文件重点：
# 1. async def 不一定是 coroutine：看里面有没有 yield。
# 2. Async Generator = yield 的产出能力 + await 的等待能力。
# 3. 不能把整个 generator 当成普通 coroutine 一次 await 完。
# 4. 惰性：async for / anext 才会往下跑。
