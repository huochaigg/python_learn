"""V12-06 asyncio.create_task()：把 coroutine 交给 Event Loop 调度。

学习目标：
1. 分清 Coroutine（计算对象）和 Task（已被调度的 coroutine）。
2. 创建 Task 后保存引用，最后 await，不要创建完就扔。
3. 观察交错的执行顺序。

运行：uv run python lessons/v12/06_create_task.py
"""

import asyncio


async def worker(name: str, delay: float) -> str:
    print(f"  {name} start")
    await asyncio.sleep(delay)
    print(f"  {name} done")
    return name


async def main() -> None:
    print("先创建两个 coroutine，还没开始跑函数体")
    coro_a = worker("A", 0.2)
    coro_b = worker("B", 0.1)

    # asyncio.create_task(coro)：
    # 用途：把 coroutine 包装成 Task，注册给当前 Event Loop 开始调度。
    # 返回：Task 对象（也 await 得得到最终结果）。
    # Coroutine 像任务描述；Task 像已经交给调度器运行的任务。
    # JS 对比：有点像「已经在跑的 Promise」，但不要直接等同。
    # 坑：创建后既不 await、也不保存引用、也不处理异常，生命周期和错误都会失控。
    # 短生命周期并发可以用 Task；需要持久化/重试/重启后继续，应走任务队列，不是 create_task。
    task_a = asyncio.create_task(coro_a)
    task_b = asyncio.create_task(coro_b)
    print("Task A =", task_a)
    print("Task B =", task_b)
    print("create_task 之后它们会被推进；B 更短，可能先 done")

    result_b = await task_b
    result_a = await task_a
    print("结果 =", result_a, result_b)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 06 create_task 运行完毕 ---")

# 本文件重点：
# 1. Coroutine 需要被调度；create_task 把它变成 Task。
# 2. 保存 Task 引用，并最终 await。
# 3. 不要把 create_task 当成可靠后台队列。
# 4. 简单「一起等完」多数时候用 gather 就够。
