"""V15 入口：把 models / repository / service / async 串成一条执行链。

学习目标：
1. 看懂分层：main -> Service -> Repository -> 内存存储。
2. 出错时 Repository 返回 None，Service raise 业务异常，main 转成 Error Response。
3. 聚合用 gather，批量用 Semaphore，流式用 Async Generator，资源用 async with。

运行（项目根目录）：
uv run python -m lessons.v15.order_app.main
"""

import asyncio
import time

from lessons.v15.order_app.exceptions import BizException
from lessons.v15.order_app.models.order import OrderItem
from lessons.v15.order_app.repositories.order_repository import OrderRepository
from lessons.v15.order_app.repositories.user_repository import UserRepository
from lessons.v15.order_app.services.order_service import OrderService, iter_order_ids
from lessons.v15.order_app.services.user_service import UserService


def print_error(exc: BizException) -> None:
    print("API Error Response =", exc.to_response())


async def main() -> None:
    user_repo = UserRepository()
    order_repo = OrderRepository()
    stock = {"sku-1": 100, "sku-2": 2}
    users = UserService(user_repo)
    orders = OrderService(order_repo, user_repo, stock)

    print("===== 1. 创建用户 =====")
    ada = await users.create_user("Ada", "admin")
    tom = await users.create_user("Tom", "user")
    await users.create_user("Jack", "user", active=False)
    all_users = await users.list_users()
    print("Ada =", ada)
    print("全部用户 =", all_users)
    print("active 名字 =", users.active_names(all_users))
    print("admins =", users.filter_users(all_users, lambda u: u.role == "admin"))

    print("\n===== 2. 创建订单 =====")
    first = await orders.create_order(
        tom.id,
        [OrderItem(sku="sku-1", qty=2, unit_price=10)],
    )
    print("created =", first)

    print("\n===== 3. 查询订单 =====")
    found = await orders.get_order(first.id)
    print("found =", found)
    listed = await orders.list_orders()
    print("订单摘要:")
    for line in orders.iter_summaries(listed):
        print(" ", line)

    print("\n===== 4. 异常场景 =====")
    try:
        await users.get_user(999)
    except BizException as exc:
        print_error(exc)

    try:
        await orders.get_order(999)
    except BizException as exc:
        print_error(exc)

    try:
        await orders.create_order(
            tom.id,
            [OrderItem(sku="sku-2", qty=99, unit_price=5)],
        )
    except BizException as extra:
        print_error(extra)

    try:
        await orders.cancel_order(first.id, current_role="user")
    except BizException as extra:
        print_error(extra)

    cancelled = await orders.cancel_order(first.id, current_role="admin")
    print("admin 取消后 status =", cancelled.status)

    print("\n===== 5. 并发获取详情 =====")
    paid = await orders.create_order(
        tom.id,
        [OrderItem(sku="sku-1", qty=1, unit_price=10)],
    )
    t0 = time.perf_counter()
    serial = await orders.get_order_detail(paid.id, concurrent=False)
    serial_cost = time.perf_counter() - t0
    print("串行 keys =", list(serial.keys()), "耗时", round(serial_cost, 3))

    t1 = time.perf_counter()
    parallel = await orders.get_order_detail(paid.id, concurrent=True)
    parallel_cost = time.perf_counter() - t1
    print("并发 shipping =", parallel["shipping"], "耗时", round(parallel_cost, 3))
    print("三个独立 IO：串行应明显慢于 gather 并发")

    print("\n===== 6. 批量限流查询 =====")
    extra_ids: list[int] = []
    for _ in range(10):
        extra = await orders.create_order(
            tom.id,
            [OrderItem(sku="sku-1", qty=1, unit_price=10)],
        )
        extra_ids.append(extra.id)
    batch_ids = list(iter_order_ids(extra_ids[0], 10))
    print("batch ids =", batch_ids)
    t2 = time.perf_counter()
    batch = await orders.get_many(batch_ids)
    print("查到", len(batch), "条, 耗时", round(time.perf_counter() - t2, 3), "s")
    print("Semaphore(3): 观察 start/end，同时大约只有 3 个在跑")

    print("\n===== 7. 流式订单状态 =====")
    async for status in orders.stream_order_status(paid.id):
        print(" status =", status)

    print("\n执行链: main -> Service -> Repository -> memory/async IO -> Model")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- v15 order_app 运行完毕 ---")

# 本文件重点：
# 1. main 只负责组装依赖和演示，业务在 Service。
# 2. 查不到: Repository 返回 None，Service raise，main 捕获 BizException。
# 3. gather 聚合独立 IO；Semaphore 限制批量并发；async for 消费状态流。
# 4. constructor 注入 Repository，为后面 FastAPI Depends 做铺垫。
