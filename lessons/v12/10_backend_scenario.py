"""V12-10 后端小场景：互不依赖的 IO 用 gather 并发。

学习目标：
1. 模拟接口同时查用户、订单、权限。
2. 对比串行 await 和 gather 的耗时与聚合结果。
3. 体会真实后端里「没有数据依赖就可以一起等」。

运行：uv run python lessons/v12/10_backend_scenario.py
"""

import asyncio
import time


async def fetch_user() -> dict:
    await asyncio.sleep(0.3)
    return {"id": 1, "name": "Ada"}


async def fetch_orders() -> list[dict]:
    await asyncio.sleep(0.4)
    return [{"id": 10, "amount": 99}]


async def fetch_permissions() -> list[str]:
    await asyncio.sleep(0.2)
    return ["orders:read"]


async def serial_dashboard() -> dict:
    user = await fetch_user()
    orders = await fetch_orders()
    perms = await fetch_permissions()
    return {"user": user, "orders": orders, "permissions": perms}


async def concurrent_dashboard() -> dict:
    user, orders, perms = await asyncio.gather(
        fetch_user(),
        fetch_orders(),
        fetch_permissions(),
    )
    return {"user": user, "orders": orders, "permissions": perms}


async def main() -> None:
    # 这三项互不依赖：没有「必须先有 user 才能查 orders」。
    # IO Bound（HTTP/DB/Redis）适合 asyncio；CPU Bound 不算力，别指望 gather 变快。
    print("=== 串行 ===")
    t0 = time.perf_counter()
    serial = await serial_dashboard()
    print(serial, "耗时", round(time.perf_counter() - t0, 2), "秒")

    print("\n=== gather 并发 ===")
    t1 = time.perf_counter()
    parallel = await concurrent_dashboard()
    print(parallel, "耗时", round(time.perf_counter() - t1, 2), "秒")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 10 后端场景 运行完毕 ---")

# 本文件重点：
# 1. 互不依赖的查询可以 gather，总等待接近最慢的那一个。
# 2. 有依赖时（先登录再凭 token 拉详情）仍要先 await 再下一步。
# 3. FastAPI 里 async def endpoint 等待 DB/HTTP 时，循环还能接别的请求。
# 4. create_task 不是 BullMQ/Celery：要持久化、重试、重启后续跑，用任务队列。
