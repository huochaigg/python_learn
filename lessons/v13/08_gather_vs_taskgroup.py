"""V13-08 gather vs TaskGroup：聚合结果 vs 结构化生命周期。

学习目标：
1. 同一组 3 个 IO，分别用 gather 和 TaskGroup 跑一遍。
2. 知道它们不是谁取代谁。
3. 简单聚合用 gather；强关联一组子任务用 TaskGroup。

运行：uv run python lessons/v13/08_gather_vs_taskgroup.py
"""

import asyncio


async def io_job(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return name


async def with_gather() -> list[str]:
    # gather：手里已有几件异步工作，把结果一起拿回来（按参数顺序）。
    a, b, c = await asyncio.gather(
        io_job("A", 0.08),
        io_job("B", 0.05),
        io_job("C", 0.1),
    )
    return [a, b, c]


async def with_taskgroup() -> list[str]:
    # TaskGroup：这些 Task 属于同一生命周期，离开块前统一管理。
    async with asyncio.TaskGroup() as tg:
        t_a = tg.create_task(io_job("A", 0.08))
        t_b = tg.create_task(io_job("B", 0.05))
        t_c = tg.create_task(io_job("C", 0.1))
    return [t_a.result(), t_b.result(), t_c.result()]


async def main() -> None:
    print("gather =", await with_gather())
    print("TaskGroup =", await with_taskgroup())


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 08 gather vs TaskGroup 运行完毕 ---")

# 本文件重点：
# 1. gather 擅长简单聚合多个结果。
# 2. TaskGroup 强调作用域和生命周期，少留孤儿 Task。
# 3. 不是绝对替代关系，场景不同。
# 4. 还要限流时，两者都可以配合 Semaphore。
