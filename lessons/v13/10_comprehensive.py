"""V13-10 综合练习：批量订单处理器。

学习目标：
1. 15 个订单、最多 4 个同时处理、单个超时 1 秒、安全更新成功数。
2. 示例答案用 Semaphore + gather；TODO 里也可改成 Queue + Consumer。
3. 先自己写，再看答案。

运行：uv run python lessons/v13/10_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

import asyncio

ORDERS = [f"o-{i}" for i in range(15)]
LIMIT = 4
TIMEOUT = 1.0


async def handle_order(order_id: str) -> str:
    """第 7、11 号故意超过 1 秒，用来触发 timeout。"""
    n = int(order_id.split("-")[1])
    delay = 1.2 if n in {7, 11} else 0.05
    await asyncio.sleep(delay)
    return order_id


# =============================================================================
# 练习 1
# TODO: 用 Semaphore(LIMIT) 包住 handle_order，gather 处理 ORDERS。
#       单个订单 async with asyncio.timeout(TIMEOUT)。
#       超时记失败，不要让整个 gather 崩掉。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


async def process_all() -> tuple[int, int]:
    sem = asyncio.Semaphore(LIMIT)
    ok = 0
    fail = 0
    lock = asyncio.Lock()

    async def one(order_id: str) -> None:
        nonlocal ok, fail
        async with sem:
            try:
                async with asyncio.timeout(TIMEOUT):
                    await handle_order(order_id)
            except TimeoutError:
                async with lock:
                    fail += 1
                return
            async with lock:
                ok += 1

    await asyncio.gather(*[one(oid) for oid in ORDERS])
    return ok, fail


# =============================================================================
# 练习 2
# TODO: 想一想 Queue + 4 个 consumer + sentinel 怎么实现同一批订单。
#       不必两套都写满，能说出 get / task_done / join 的分工即可。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")
print("Queue: producer put 15 个订单；4 个 consumer get 后处理。")
print("get 只是领到任务；处理完 task_done；producer/main join 等全部完成。")
print("然后再给每个 consumer 一个 None sentinel 让它们退出。")


async def main() -> None:
    ok, fail = await process_all()
    print("success =", ok, "failed =", fail)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 10 综合练习 运行完毕 ---")

# 本文件重点：
# 1. Semaphore 限同时 4 个；timeout 限单个 1 秒。
# 2. 成功数是共享状态，更新时用 Lock（或避免共享）。
# 3. 失败要记下来，不要让整批 gather 直接炸。
# 4. Queue+Consumer 是同一问题的另一种编排。
