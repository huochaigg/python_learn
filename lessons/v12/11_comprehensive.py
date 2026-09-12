"""V12-11 综合练习：同时请求多个商品详情。

学习目标：
1. 综合 async def、await、run、create_task、gather、异常、耗时对比。
2. 先 TODO，再对照示例答案。
3. 场景：拉 3 个商品详情，其中一个会失败。

运行：uv run python lessons/v12/11_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

import asyncio
import time


async def fetch_product(pid: str, delay: float, fail: bool = False) -> dict:
    await asyncio.sleep(delay)
    if fail:
        raise ValueError(f"product {pid} not found")
    return {"id": pid, "title": f"item-{pid}"}


# =============================================================================
# 练习 1
# TODO: 写 async def main_sequential()，依次 await p1 / p2 / p3（都不失败）。
#       用 perf_counter 打印总耗时。delay 用 0.2。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


async def main_sequential() -> list[dict]:
    t0 = time.perf_counter()
    a = await fetch_product("1", 0.2)
    b = await fetch_product("2", 0.2)
    c = await fetch_product("3", 0.2)
    print("串行结果 =", [a, b, c], "耗时", round(time.perf_counter() - t0, 2))
    return [a, b, c]


# =============================================================================
# 练习 2
# TODO: 用 gather 并发拉同样三个商品，打印耗时（应接近 0.2 而不是 0.6）。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


async def main_gather() -> list[dict]:
    t0 = time.perf_counter()
    items = await asyncio.gather(
        fetch_product("1", 0.2),
        fetch_product("2", 0.2),
        fetch_product("3", 0.2),
    )
    print("gather 结果 =", items, "耗时", round(time.perf_counter() - t0, 2))
    return list(items)


# =============================================================================
# 练习 3
# TODO: 用 create_task 启动两个 fetch，保存引用后分别 await。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


async def main_tasks() -> list[dict]:
    t1 = asyncio.create_task(fetch_product("8", 0.15))
    t2 = asyncio.create_task(fetch_product("9", 0.15))
    return [await t1, await t2]


# =============================================================================
# 练习 4
# TODO: gather 三个任务，其中 pid=2 fail=True。
#       先体验默认抛错；再 return_exceptions=True 并检查异常项。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


async def main_errors() -> None:
    try:
        await asyncio.gather(
            fetch_product("1", 0.05),
            fetch_product("2", 0.05, fail=True),
            fetch_product("3", 0.05),
        )
    except ValueError as e:
        print("默认 gather 抛错 =", e)

    mixed = await asyncio.gather(
        fetch_product("1", 0.05),
        fetch_product("2", 0.05, fail=True),
        fetch_product("3", 0.05),
        return_exceptions=True,
    )
    print("return_exceptions =", mixed)


async def main() -> None:
    await main_sequential()
    await main_gather()
    print("create_task 结果 =", await main_tasks())
    await main_errors()


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 11 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 调用 async def 得到 coroutine，要 await / Task / run 才执行。
# 2. 连续 await 仍串行；gather / create_task 才能一起等 IO。
# 3. 保存 Task 并 await；失败用 try/except 或显式检查 return_exceptions。
# 4. 入口仍然是 asyncio.run(main())。
