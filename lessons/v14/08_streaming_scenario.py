"""V14-08 流式 Demo：token 边到边打印。

学习目标：
1. Async Generator 等待 → yield chunk，调用端 async for 立刻看到。
2. 对比「等全部拼完再 return」。
3. 联系 AI streaming / SSE，但不发真实网络请求。

运行：uv run python lessons/v14/08_streaming_scenario.py
"""

import asyncio
import time


async def complete_message() -> str:
    chunks = ["Hello", " ", "Python", " ", "Agent"]
    parts: list[str] = []
    for chunk in chunks:
        await asyncio.sleep(0.08)
        parts.append(chunk)
    return "".join(parts)


async def stream_message():
    chunks = ["Hello", " ", "Python", " ", "Agent"]
    for chunk in chunks:
        await asyncio.sleep(0.08)
        yield chunk


async def main() -> None:
    print("=== 一次性 return：首个可见结果要等全文 ===")
    t0 = time.perf_counter()
    text = await complete_message()
    print("  全文 =", text, "耗时", round(time.perf_counter() - t0, 2))

    print("\n=== 流式 yield：每来一块就打印 ===")
    t1 = time.perf_counter()
    seen: list[str] = []
    first_at: float | None = None
    async for chunk in stream_message():
        if first_at is None:
            first_at = time.perf_counter() - t1
        seen.append(chunk)
        print("  此刻 =", "".join(seen), "t=", round(time.perf_counter() - t1, 2))
    print("  首块耗时", round(first_at or 0, 2), "全文仍是", "".join(seen))

    # Async Generator 适合：AI token streaming、SSE、WebSocket、数据库流式结果。
    # 这里只模拟数据，不安装 FastAPI，也不接真模型。


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 08 流式场景 运行完毕 ---")

# 本文件重点：
# 1. 等全文 return，首字节也要等最慢的那段。
# 2. async for + yield 可以边收边展示。
# 3. 这就是 SSE / Agent streaming 的同步心智模型的异步版。
# 4. 本课没有真 HTTP。
