"""V12-03 await asyncio.sleep()：非阻塞等待。

学习目标：
1. 会用 asyncio.sleep 模拟 IO 等待。
2. 理解 await 是暂停当前 coroutine，把执行权交回 Event Loop。
3. 记住 time.sleep 是阻塞线程；本文件不制造长时间阻塞。

运行：uv run python lessons/v12/03_await_sleep.py
"""

import asyncio


async def load_user() -> str:
    print("开始等 IO（模拟查库）")
    # asyncio.sleep(delay)：异步非阻塞等待 delay 秒。
    # 用途：学习时模拟网络/数据库等待；生产里你 await 的是真正的异步 IO。
    # 等待期间：当前 coroutine 暂停，Event Loop 可以去跑别的 Task。
    # 不会像 time.sleep() 那样把整个线程卡住。
    # JS 对比：有点像 await new Promise(r => setTimeout(r, ms))
    await asyncio.sleep(0.2)
    print("IO 结束，恢复执行")
    return "user=Ada"


async def main() -> None:
    user = await load_user()
    print("结果 =", user)
    # 概念对比：time.sleep(0.2) 会阻塞当前线程，Event Loop 上的其他任务也跑不动。
    # 这个区别 08 会用小 Demo 亲眼看。不要在 async 代码里随手 time.sleep。


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 03 await sleep 运行完毕 ---")

# 本文件重点：
# 1. await 的核心不是「把线程卡死等」，而是暂停 coroutine、让出执行权。
# 2. asyncio.sleep 适合模拟 IO Bound 等待。
# 3. time.sleep 是同步阻塞，放到 Event Loop 线程里很危险。
# 4. 等的是 IO 时，CPU 本可以去干别的 coroutine。
