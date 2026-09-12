"""V12-01 async def / await 基础。

学习目标：
1. 对比普通 def 和 async def。
2. 看到调用 async 函数得到的是 Coroutine Object。
3. 必须 await（或交给 Event Loop）才拿得到最终结果。

运行：uv run python lessons/v12/01_async_basics.py
"""

import asyncio


def sync_get_user() -> str:
    """普通函数：调用后立刻执行完，直接返回结果。"""
    return "Tom"


async def get_user() -> str:
    # async def：定义协程函数（coroutine function）。
    # 调用 get_user() 返回 Coroutine Object，不是 "Tom"。
    # JS/TS 对比：JS async function 调用会立刻返回 Promise，并开始执行到第一个 await。
    # Python：默认不会像 Promise 那样「一创建就按同样方式自动跑」，通常要 await 或变成 Task。
    return "Ada"


async def main() -> None:
    print("同步调用直接拿结果 =", sync_get_user())

    coro = get_user()
    print("async 调用 type =", type(coro))
    print("这还不是最终用户名，只是 coroutine")

    # await：暂停当前 coroutine，等右边那个 coroutine 跑完，拿到它的返回值。
    # 这里右边很快结束，看起来几乎立刻得到 "Ada"。
    user = await coro
    print("await 之后才是结果 =", user)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 01 async 基础 运行完毕 ---")

# 本文件重点：
# 1. async def 调用 → Coroutine，不是最终结果。
# 2. 必须 await / Task / Event Loop 才会真正推进执行。
# 3. 不 await 会留下 “coroutine was never awaited” 一类问题。
# 4. 和 JS Promise 只是概念相近，不能完全画等号。
