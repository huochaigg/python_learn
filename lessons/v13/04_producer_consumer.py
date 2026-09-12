"""V13-04 生产者 / 消费者：get ≠ 完成，要 task_done + join。

学习目标：
1. producer 放任务，多个 consumer 并发处理。
2. 用 task_done / join 等待「处理完」而不只是「取走」。
3. 用 sentinel（None）干净结束 consumer。

运行：uv run python lessons/v13/04_producer_consumer.py
"""

import asyncio

WORKER_N = 3
JOB_N = 10


async def producer(queue: asyncio.Queue[str | None]) -> None:
    for i in range(JOB_N):
        await queue.put(f"order-{i}")
        print("produced", f"order-{i}")
    # 等 10 个真实任务都被 task_done，再发结束信号。
    await queue.join()
    for _ in range(WORKER_N):
        # sentinel pattern：放入约定好的结束值（这里是 None）。
        # 每个 consumer 拿到 None 就退出，避免 worker 永远卡在 get 上。
        await queue.put(None)


async def consumer(name: str, queue: asyncio.Queue[str | None]) -> None:
    while True:
        item = await queue.get()
        try:
            if item is None:
                print(name, "收到 sentinel，退出")
                break
            print(name, "处理", item)
            await asyncio.sleep(0.05)
        finally:
            # task_done()：标记「这个 get 到的 item 已经处理完」。
            # get 只表示取到任务，像 Worker 领到 Job，还不等于 completed。
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    workers = [
        asyncio.create_task(consumer(f"w{i}", queue))
        for i in range(WORKER_N)
    ]
    await producer(queue)
    await asyncio.gather(*workers)
    print("全部结束")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 04 生产者消费者 运行完毕 ---")

# 本文件重点：
# 1. get 拿走任务；task_done 才表示处理结束。
# 2. join 等待「已入队且未 done」的数量归零。
# 3. sentinel（None）用来规范结束 consumer。
# 4. 这是进程内协作，不是 BullMQ。
