"""V13-01 Semaphore：限制同时执行的数量。

学习目标：
1. 会用 asyncio.Semaphore(n) 做并发上限。
2. 用 async with 获取/释放 permit。
3. 看到 10 个请求最多同时跑 3 个。

运行：uv run python lessons/v13/01_semaphore.py
"""

import asyncio
import time

LIMIT = 3
# asyncio.Semaphore(n)：有限数量的 permit（令牌）。
# 用途：限制同时进入某段代码的 coroutine 数，类似「最多 3 个并发 HTTP」。
# 进入 async with 时获取 1 个；退出（含异常）时自动释放。
# 这是 Async Context Manager，把 V6 的 with 和 V12 的 async 串起来。
# gather 负责「等全部结束」；Semaphore 负责「同时最多几个」。两者不冲突。
semaphore = asyncio.Semaphore(LIMIT)

current_running = 0
max_running = 0


async def fetch(i: int) -> str:
    global current_running, max_running
    async with semaphore:
        current_running += 1
        if current_running > max_running:
            max_running = current_running
        # 上面两行之间没有 await，当前 Demo 里计数不会被切开。
        # 真实项目不要为了统计随便引入未保护的复杂共享状态。
        print(f"start #{i} running={current_running} t={time.perf_counter():.2f}")
        await asyncio.sleep(0.15)
        print(f"end   #{i} t={time.perf_counter():.2f}")
        current_running -= 1
        return f"ok-{i}"


async def main() -> None:
    results = await asyncio.gather(*[fetch(i) for i in range(10)])
    print("results =", results)
    print("max_running =", max_running, "limit =", LIMIT)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 01 Semaphore 运行完毕 ---")

# 本文件重点：
# 1. Semaphore(n) ≈ 并发令牌池，最多 n 个同时进入。
# 2. async with semaphore 会自动获取/释放。
# 3. gather 等全部；Semaphore 限同时跑多少，两个维度不同。
# 4. 进程内限流 ≠ Redis/BullMQ 分布式队列。
