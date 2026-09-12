"""V13-05 超时：不允许某个 await 永远等下去。

学习目标：
1. 优先用 Python 3.12 的 asyncio.timeout()。
2. 认识现有代码里常见的 wait_for。
3. 超时会得到 TimeoutError。

运行：uv run python lessons/v13/05_timeout.py
"""

import asyncio


async def fast() -> str:
    await asyncio.sleep(0.05)
    return "fast-ok"


async def slow() -> str:
    await asyncio.sleep(0.4)
    return "slow-ok"


async def main() -> None:
    print("1) asyncio.timeout：超时时间内完成")
    # asyncio.timeout(delay)：异步超时上下文。
    # 进入后，块里的 await 加起来超过 delay 秒会抛 TimeoutError。
    # 用途：HTTP / DB 不能无限等。退出时自动解除超时。
    async with asyncio.timeout(0.2):
        print("  ", await fast())

    print("2) 慢任务超过 timeout")
    try:
        async with asyncio.timeout(0.1):
            await slow()
    except TimeoutError as e:
        print("  TimeoutError =", type(e).__name__)

    print("3) asyncio.wait_for：老写法，现有项目仍常见")
    # wait_for(coro, timeout=秒)：给单个 coroutine 设上限，超时同样 TimeoutError。
    try:
        print("  ", await asyncio.wait_for(fast(), timeout=0.2))
        await asyncio.wait_for(slow(), timeout=0.1)
    except TimeoutError:
        print("  wait_for 也超时")


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 05 timeout 运行完毕 ---")

# 本文件重点：
# 1. 真实 IO 必须设超时，不能干等。
# 2. 3.12 优先 async with asyncio.timeout(...) 。
# 3. wait_for(coro, timeout=...) 是常见等价手段。
# 4. 超时抛 TimeoutError（别和自己的业务异常混为一谈）。
