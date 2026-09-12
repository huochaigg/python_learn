"""V12-05 async 不等于并发：顺序 await vs 并发等待。

学习目标：
1. 三个 sleep(1) 依次 await，总时间大约 3 秒。
2. 并发后总时间大约 1 秒多。
3. 用 perf_counter 看耗时，记住：写成 async 不会自动一起跑。

运行：uv run python lessons/v12/05_sequential_vs_concurrent.py
"""

import asyncio
import time


async def fetch_a() -> str:
    print("A start")
    await asyncio.sleep(1)
    print("A done")
    return "A"


async def fetch_b() -> str:
    print("B start")
    await asyncio.sleep(1)
    print("B done")
    return "B"


async def fetch_c() -> str:
    print("C start")
    await asyncio.sleep(1)
    print("C done")
    return "C"


async def sequential() -> list[str]:
    a = await fetch_a()
    b = await fetch_b()
    c = await fetch_c()
    return [a, b, c]


async def concurrent() -> list[str]:
    return list(await asyncio.gather(fetch_a(), fetch_b(), fetch_c()))


async def main() -> None:
    # time.perf_counter()：单调时钟，适合测时间间隔，不适合当「墙上时钟」。
    print("=== 顺序 await：A 完再 B 再 C ===")
    t0 = time.perf_counter()
    seq = await sequential()
    print("结果 =", seq, "耗时 =", round(time.perf_counter() - t0, 2), "秒")

    print("\n=== gather 并发：三个 IO 同时处于等待 ===")
    t1 = time.perf_counter()
    par = await concurrent()
    print("结果 =", par, "耗时 =", round(time.perf_counter() - t1, 2), "秒")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 05 顺序 vs 并发 运行完毕 ---")

# 本文件重点：
# 1. async ≠ 自动并发。连续 await a(); await b(); 仍是串行。
# 2. 多个 IO 要同时等，需要 gather / Task。
# 3. 三个 1 秒 IO：串行 ~3s，并发 ~1s。
# 4. 这是 IO Bound 的收益，不是三核 CPU 一起算。
