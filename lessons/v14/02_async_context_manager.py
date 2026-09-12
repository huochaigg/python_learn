"""V14-02 手写 Async Context Manager：__aenter__ / __aexit__。

学习目标：
1. 对照 V6 的 __enter__/__exit__，看清多了一个 a（async）。
2. 代码块里抛异常时，__aexit__ 仍然会跑。
3. 知道 __aexit__ 返回值能影响异常传播，本课不展开。

运行：uv run python lessons/v14/02_async_context_manager.py
"""

import asyncio


class AsyncDatabaseConnection:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.opened = False

    async def __aenter__(self) -> "AsyncDatabaseConnection":
        # __aenter__：进入 async with 时会被 await。
        # 用途：异步获取资源（连库、开事务、拿 HTTP session）。
        # 返回值：出现在 as 后面。这里返回 self。
        # 对比 V6：__enter__ 是同步的，这里可以 await。
        print("connect", self.dsn)
        await asyncio.sleep(0.05)
        self.opened = True
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        # __aexit__：离开 async with 时会被 await，无论成功还是异常。
        # 参数：和同步 __exit__ 一样，没异常时三个都是 None。
        # 返回值：本课返回 None，异常继续往外传。返回 True 可以吞掉异常，先不展开。
        print("close, opened =", self.opened, "exc_type =", exc_type)
        await asyncio.sleep(0.05)
        self.opened = False

    async def query(self, sql: str) -> str:
        return f"rows from {sql}"


async def main() -> None:
    print("=== 正常路径 ===")
    async with AsyncDatabaseConnection("postgres://local") as db:
        print("query =", await db.query("select 1"))

    print("\n=== 块内抛错：__aexit__ 仍会执行（串起 V5 finally / V6 with）===")
    try:
        async with AsyncDatabaseConnection("postgres://local") as db:
            print("query 前")
            raise ValueError("boom")
    except ValueError as e:
        print("外层捕获 =", e)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 02 Async Context Manager 运行完毕 ---")

# 本文件重点：
# 1. async with → await __aenter__ → 代码块 → await __aexit__。
# 2. 对应同步 with → __enter__ → 代码块 → __exit__。
# 3. 内部抛错也会走 __aexit__，和 finally 一样保清理。
# 4. 返回值能否吞异常本课先记住「有这回事」。
