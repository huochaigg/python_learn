"""V13-03 asyncio.Queue 基础：进程内、内存里的异步队列。

学习目标：
1. 会 put / get / qsize。
2. 知道它只在当前进程、当前 Event Loop 里传数据。
3. 不要把它当成 Redis / BullMQ / Celery。

运行：uv run python lessons/v13/03_queue_basics.py
"""

import asyncio


async def main() -> None:
    # asyncio.Queue：coroutine 之间传递数据的内存队列。
    # 用途：生产者放入、消费者取出；可设 maxsize 做有界队列。
    # put/get 都是 await：队列满/空时暂停当前 coroutine，不堵 Event Loop。
    # 不是可靠任务系统：进程退出或重启，里面的 item 就没了。
    queue: asyncio.Queue[str] = asyncio.Queue()

    await queue.put("order-1")
    await queue.put("order-2")
    print("qsize after put =", queue.qsize())

    first = await queue.get()
    print("get =", first, "qsize =", queue.qsize())
    second = await queue.get()
    print("get =", second, "qsize =", queue.qsize())


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 03 Queue 基础 运行完毕 ---")

# 本文件重点：
# 1. Queue 适合单进程内部 coroutine 协作。
# 2. put 放入，get 取出；qsize 看大约积压多少。
# 3. 重启即丢失，不能替代 Redis 队列。
# 4. get 不等于处理完成，下一课才讲 task_done / join。
