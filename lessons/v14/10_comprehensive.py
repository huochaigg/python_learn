"""V14-10 综合练习：异步订单流。

学习目标：
1. 综合 async with、__aenter__/__aexit__、Async Generator、async for、await。
2. 进入模拟 DB 连接后按间隔产出订单，消费到一定数量结束。
3. 先 TODO，再看示例答案。

运行：uv run python lessons/v14/10_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

import asyncio


# =============================================================================
# 练习 1
# TODO: 写 class AsyncDB：
#       async def __aenter__ 里 print("connect") 并 return self
#       async def __aexit__ 里 print("close")
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


class AsyncDB:
    async def __aenter__(self) -> "AsyncDB":
        print("connect")
        await asyncio.sleep(0.02)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        print("close")
        await asyncio.sleep(0.02)


# =============================================================================
# 练习 2
# TODO: 写 async def order_stream(n)：await 一小段再 yield "o-1" ...。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


async def order_stream(n: int):
    for i in range(1, n + 1):
        await asyncio.sleep(0.04)
        yield f"o-{i}"


# =============================================================================
# 练习 3
# TODO: async with AsyncDB()，再 async for 消费 order_stream(5)，
#       收到 3 条就 break。确认 close 仍然发生。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


async def main() -> None:
    seen: list[str] = []
    async with AsyncDB() as db:
        print("using", type(db).__name__)
        async for oid in order_stream(5):
            print("got", oid)
            seen.append(oid)
            if len(seen) >= 3:
                break
    print("seen =", seen)
    print(
        "\n对照: with <-> async with; __enter__/__exit__ <-> __aenter__/__aexit__; "
        "for <-> async for; __iter__/__next__ <-> __aiter__/__anext__; "
        "StopIteration <-> StopAsyncIteration; def+yield <-> async def+yield"
    )


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 10 综合练习 运行完毕 ---")

# 本文件重点：
# 1. async with + __aenter__/__aexit__ 进入/退出连接。
# 2. async def + yield 产出订单流。
# 3. async for 消费；break 后 with 仍会 close。
# 4. 同步/异步协议对照：
#    with ↔ async with
#    __enter__/__exit__ ↔ __aenter__/__aexit__
#    for ↔ async for
#    __iter__/__next__ ↔ __aiter__/__anext__
#    StopIteration ↔ StopAsyncIteration
#    def + yield ↔ async def + yield
