"""V13-06 Task 取消：协作式，不是杀进程。

学习目标：
1. 会 create_task → 跑一会儿 → cancel → await。
2. 在 CancelledError / finally 里做清理。
3. 清理后通常还要 raise，不要把取消吞掉。

运行：uv run python lessons/v13/06_task_cancel.py
"""

import asyncio


async def long_job() -> None:
    print("long_job 开始")
    try:
        n = 0
        while True:
            print("  tick", n)
            n += 1
            await asyncio.sleep(0.15)
    except asyncio.CancelledError:
        # CancelledError：协作式取消信号，通常在某个 await 点注入。
        # cancel() 不是立刻物理掐死线程，而是请求任务在安全点停下来。
        print("  收到 CancelledError，做清理后继续 raise")
        raise
    finally:
        print("  finally：释放锁/连接/临时资源")


async def main() -> None:
    task = asyncio.create_task(long_job())
    await asyncio.sleep(0.4)
    print("main 调用 task.cancel()")
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("main 确认：任务确实被取消")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 06 Task 取消 运行完毕 ---")

# 本文件重点：
# 1. cancel() 是请求取消，在 await 点生效。
# 2. finally 保证被取消时也清理资源。
# 3. 捕获 CancelledError 做完清理后通常再 raise。
# 4. 吞掉取消会导致上层以为停了、实际还在跑。
