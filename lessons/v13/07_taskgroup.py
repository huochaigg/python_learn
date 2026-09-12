"""V13-07 TaskGroup：结构化并发。

学习目标：
1. 用 async with TaskGroup + tg.create_task 管理一组相关任务。
2. 看到其中一个失败时，整组生命周期会被一起收掉。
3. 眼熟 ExceptionGroup，不展开 except*。

运行：uv run python lessons/v13/07_taskgroup.py
"""

import asyncio


async def ok(name: str, delay: float) -> str:
    print(name, "start")
    try:
        await asyncio.sleep(delay)
        print(name, "done")
        return name
    except asyncio.CancelledError:
        print(name, "被取消")
        raise


async def boom() -> str:
    await asyncio.sleep(0.08)
    raise ValueError("child failed")


async def main() -> None:
    print("=== 全部成功 ===")
    # asyncio.TaskGroup：结构化并发。
    # 一组子任务限定在这个 async with 作用域内；离开块之前会等它们结束。
    # tg.create_task(coro) 在组内创建 Task，比满地 create_task 更不容易留孤儿。
    async with asyncio.TaskGroup() as tg:
        tg.create_task(ok("A", 0.1))
        tg.create_task(ok("B", 0.15))
    print("组正常退出")

    print("\n=== 一个失败：同组其他任务通常会被取消 ===")
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(ok("C", 0.4))
            tg.create_task(boom())
            tg.create_task(ok("D", 0.4))
    except ExceptionGroup as eg:
        # ExceptionGroup：一组任务的多个异常被包在一起抛出。
        # 本课只认识它；完整 except* 语法以后需要再学。
        print("ExceptionGroup 异常个数 =", len(eg.exceptions))
        print("  内容 =", eg.exceptions)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 07 TaskGroup 运行完毕 ---")

# 本文件重点：
# 1. TaskGroup 把相关 Task 放进明确作用域。
# 2. 离开 with 前会统一收尾，减少「忘了 await」的孤儿任务。
# 3. 一个失败会影响整组生命周期。
# 4. 失败时可能看到 ExceptionGroup。
