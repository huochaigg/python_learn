"""V12-08 阻塞 API 会堵住 Event Loop。

学习目标：
1. 对比 asyncio.sleep 和 time.sleep 对其它 Task 的影响。
2. 时间控制在约 1 秒内，能看清交错差异即可。
3. 记住：async 函数里的同步阻塞，会卡住整个循环。

运行：uv run python lessons/v12/08_blocking_problem.py
"""

import asyncio
import time


async def heartbeat(tag: str) -> None:
    for i in range(4):
        print(f"  heartbeat {tag} #{i}")
        await asyncio.sleep(0.2)


async def nice_wait() -> None:
    print("nice_wait: asyncio.sleep 0.6s，会让出执行权")
    await asyncio.sleep(0.6)
    print("nice_wait: 结束")


async def bad_wait() -> None:
    print("bad_wait: time.sleep 0.6s，堵住当前线程/Event Loop")
    # time.sleep：同步阻塞当前线程。
    # 在 Event Loop 所在线程调用时，其它 coroutine 这段时间基本跑不动。
    # 类似 Node 主线程被同步重活占满。
    time.sleep(0.6)
    print("bad_wait: 结束")


async def main() -> None:
    print("=== 非阻塞：heartbeat 能穿插 ===")
    await asyncio.gather(heartbeat("A"), nice_wait())

    print("\n=== 阻塞：heartbeat 会在 sleep 期间卡住 ===")
    await asyncio.gather(heartbeat("B"), bad_wait())


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 08 阻塞问题 运行完毕 ---")

# 本文件重点：
# 1. asyncio.sleep 暂停当前 coroutine，别人还能跑。
# 2. time.sleep 堵住 Event Loop，别人也停。
# 3. asyncio 适合 IO Bound；CPU 大循环同样会堵循环。
# 4. 本版不引入线程池/进程池，先把坑认出来。
