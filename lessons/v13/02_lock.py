"""V13-02 Lock：await 交错仍可能有 Race Condition。

学习目标：
1. 看到「读 → await → 写」会被其他 Task 插入。
2. 用 async with lock 保护临界区。
3. 明白单线程 Event Loop ≠ 没有竞态。

运行：uv run python lessons/v13/02_lock.py
"""

import asyncio

count = 0
# asyncio.Lock()：coroutine 之间的互斥锁。
# 用途：同一时刻只允许一个 coroutine 进入 async with lock 区域。
# 不是 threading.Lock，不要混用；线程锁以后再讲。
# 进入时获取；退出（含异常）时释放。
lock = asyncio.Lock()


async def unsafe_add() -> None:
    global count
    value = count
    await asyncio.sleep(0)
    count = value + 1


async def safe_add() -> None:
    global count
    async with lock:
        value = count
        await asyncio.sleep(0)
        count = value + 1


async def main() -> None:
    global count
    n = 50

    count = 0
    await asyncio.gather(*[unsafe_add() for _ in range(n)])
    print("无锁累加，期望", n, "实际", count, "（读和写之间 await，别人插队）")

    count = 0
    await asyncio.gather(*[safe_add() for _ in range(n)])
    print("有锁累加，期望", n, "实际", count)

    # 单线程也会竞态：coroutine 在 await 处让出执行权。
    # 更优先的做法往往是减少共享可变状态，而不是到处加锁。


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 02 Lock 运行完毕 ---")

# 本文件重点：
# 1. asyncio 单线程仍可能有 Race Condition。
# 2. 危险模式：读取共享状态 → await → 再写回。
# 3. asyncio.Lock 保护 coroutine 临界区，不是线程锁。
# 4. Lock ≈ 同时只准 1 个；Semaphore ≈ 同时准 N 个。
