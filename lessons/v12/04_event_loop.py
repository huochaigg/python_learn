"""V12-04 Event Loop 与 asyncio.run()。

学习目标：
1. 知道普通脚本用 asyncio.run(main()) 当入口。
2. 理解它会创建/运行/清理 Event Loop。
3. 知道 FastAPI 已经自己管循环，请求里不要再乱 asyncio.run()。

运行：uv run python lessons/v12/04_event_loop.py
"""

import asyncio


async def main() -> None:
    print("main coroutine 正在 Event Loop 里运行")
    await asyncio.sleep(0.05)
    print("await 回来之后继续 main")


# ---------------------------------------------------------------------------
# Event Loop：调度 coroutine / Task、等待 IO、在就绪时恢复执行。
# 高层思路和 Node Event Loop 类似：一个任务在等 IO 时，先去跑别的任务。
# 实现细节不要当成完全一样。
#
# asyncio.run(coro)：
# 用途：普通脚本里启动事件循环，跑完传入的 coroutine。
# 大致：创建 loop → 运行 main → 等它结束 → 清理。
# 参数：一个 coroutine（通常是 main()）。
# 返回：该 coroutine 的返回值。
# 坑：已经在跑的 loop 里再 asyncio.run() 会报错。
# 后续 FastAPI 服务器自己已经有 Event Loop，endpoint 里直接 await 即可，
# 不要在请求处理中再随便 asyncio.run()。
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 04 Event Loop 运行完毕 ---")

# 本文件重点：
# 1. 学习脚本入口：async def main() + asyncio.run(main())。
# 2. 最外层不能随便写 await main()。
# 3. FastAPI 场景下循环已经在跑，业务代码只 await。
# 4. Event Loop 负责「等 IO 时切换任务」，不是多核并行。
