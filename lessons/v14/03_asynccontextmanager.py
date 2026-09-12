"""V14-03 @asynccontextmanager：用 Async Generator 写异步资源管理。

学习目标：
1. 不用手写 __aenter__/__aexit__，也能做 async with。
2. 看懂 yield 前=进入，yield 出资源，yield 后=清理。
3. 把 V9 Generator、V11 Decorator、V14 async with 串起来。

运行：uv run python lessons/v14/03_asynccontextmanager.py
"""

import asyncio
from contextlib import asynccontextmanager


# @asynccontextmanager：装饰一个 async generator function，把它变成 Async Context Manager。
# 输入：带 yield 的 async def；输出：能用于 async with 的包装器。
# yield 前：类似 __aenter__（连接、加锁）。
# yield 出去的值：就是 as xxx 拿到的资源。
# yield 后：类似 __aexit__/finally（关闭、解锁）。块内抛错时这段仍应执行。
# 这把 V11 的 decorator、V9 的 yield、V14 的异步资源协议接在一起。
@asynccontextmanager
async def redis_client(url: str):
    print("connect", url)
    await asyncio.sleep(0.05)
    client = {"url": url, "ok": True}
    try:
        yield client
    finally:
        print("close", url)
        await asyncio.sleep(0.05)


async def main() -> None:
    print("=== 正常 ===")
    async with redis_client("redis://local") as r:
        print("as 拿到 =", r)

    print("\n=== 块内异常，close 仍然发生 ===")
    try:
        async with redis_client("redis://local") as r:
            print("拿到后准备出错", r["ok"])
            raise RuntimeError("set failed")
    except RuntimeError as e:
        print("外层捕获 =", e)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 03 asynccontextmanager 运行完毕 ---")

# 本文件重点：
# 1. @asynccontextmanager 用 async generator 实现 async with。
# 2. yield 前进入、yield 出资源、yield 后清理。
# 3. 清理放 finally，异常路径也会关连接。
# 4. FastAPI 生命周期管理里也会见到类似思想。
