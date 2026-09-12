"""V12-02 Coroutine：调用 async 函数只是得到「异步计算对象」。

学习目标：
1. 用日志证明：创建 coroutine 时函数体还没跑。
2. 只有 await（或变成 Task）之后才会进入函数体。
3. 分清 Python Coroutine 和 JS Promise 的启动时机不同。

运行：uv run python lessons/v12/02_coroutine.py
"""

import asyncio


async def fetch_profile() -> str:
    print("  [fetch_profile] 函数体开始执行")
    return "profile: Ada"


async def main() -> None:
    print("1) 调用 fetch_profile()")
    coro = fetch_profile()
    print("2) 拿到 Coroutine Object =", coro)
    print("3) 注意：上面还没有打印「函数体开始执行」")
    print("4) 现在 await，才把执行权交给它")
    result = await coro
    print("5) 结果 =", result)

    # JS 对照（概念，不是代码）：
    # async function fetchProfile() { console.log("start"); return "Ada" }
    # const p = fetchProfile()  // 通常已经开始跑，p 是 Promise
    # Python 这里：fetch_profile() 只创建 coroutine，默认不会自动按 Promise 那套启动。


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 02 Coroutine 运行完毕 ---")

# 本文件重点：
# 1. Coroutine = 可以暂停/恢复的异步计算对象。
# 2. 创建 ≠ 执行；await 或 Task 才会推进。
# 3. 和 V9 Generator「暂停/恢复」思想相近，但围绕的是 await，不是 yield 数据流。
# 4. 不要把 Coroutine 直接当成 JS Promise。
