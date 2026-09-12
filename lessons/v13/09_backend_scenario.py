"""V13-09 后端场景：批量 IO + 限流 + 超时 + 失败统计。

学习目标：
1. 20 个任务，Semaphore(3) 限制第三方 API 并发。
2. 单个调用 timeout，失败记录下来，脚本不整体崩掉。
3. 分清：进程内 Semaphore ≠ BullMQ/Celery。

运行：uv run python lessons/v13/09_backend_scenario.py
"""

import asyncio

SEM = asyncio.Semaphore(3)


async def generate_image(job_id: int) -> str:
    """模拟第三方生图/查订单：有的慢，有的直接失败。"""
    async with SEM:
        delay = 0.05 if job_id % 7 else 0.35
        fail = job_id % 5 == 0
        async with asyncio.timeout(0.2):
            await asyncio.sleep(delay)
            if fail:
                raise ValueError(f"provider error job={job_id}")
            return f"image-{job_id}"


async def run_job(job_id: int) -> tuple[int, str, str | None]:
    try:
        url = await generate_image(job_id)
        return job_id, "ok", url
    except TimeoutError:
        return job_id, "timeout", None
    except ValueError as e:
        return job_id, "error", str(e)


async def main() -> None:
    # 和「AI 生图排队 + 最大并发」是同一类问题：
    # 20 个 job 可以一起挂上，但第三方同时只准 3 个。
    jobs = [run_job(i) for i in range(20)]
    results = await asyncio.gather(*jobs)

    ok_n = sum(1 for _, status, _ in results if status == "ok")
    fail_n = len(results) - ok_n
    print("sample =", results[:5], "...")
    print("success =", ok_n, "failed =", fail_n)

    # Semaphore 只控制当前 Python 进程内并发。
    # 服务器重启、跨 Worker 共享 Job、失败重试、持久化 → 仍要任务队列。


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 09 后端场景 运行完毕 ---")

# 本文件重点：
# 1. gather 挂全部任务；Semaphore 限制同时打第三方。
# 2. timeout 防止单个调用卡死。
# 3. 每任务自己吞 TimeoutError/业务错误，整批还能出统计。
# 4. 这还不是分布式队列。
