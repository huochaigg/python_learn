"""V14-07 anext()：异步版 next()。

学习目标：
1. 手动 await anext(agen) 取值。
2. 耗尽时遇到 StopAsyncIteration。
3. 对照 V9 的 next()。

运行：uv run python lessons/v14/07_anext.py
"""

import asyncio


async def tokens():
    yield "Hello"
    yield "Python"


async def main() -> None:
    agen = tokens()
    # anext(async_iterator)：取下一项，返回 awaitable，所以必须 await。
    # 对比 V9：next(iterator) 是同步取下一项。
    print("anext 1 =", await anext(agen))
    print("anext 2 =", await anext(agen))
    try:
        await anext(agen)
    except StopAsyncIteration:
        print("第三次：StopAsyncIteration")

    agen2 = tokens()
    print("anext(..., default) =", await anext(agen2, "empty"))
    print("anext(..., default) =", await anext(agen2, "empty"))
    print("耗尽后默认值 =", await anext(agen2, "empty"))


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 07 anext 运行完毕 ---")

# 本文件重点：
# 1. next → 同步；anext → 异步，要 await。
# 2. 耗尽抛 StopAsyncIteration。
# 3. anext(it, default) 和 next(it, default) 一样可给默认值。
# 4. 日常仍优先 async for，不必手写循环。
