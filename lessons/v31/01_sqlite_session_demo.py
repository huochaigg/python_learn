"""
文件作用：用官方 SQLiteSession 做两轮对话，再观察 get_items / pop_item / clear_session。
实际意义：Agent 不会跨 HTTP 记住上一次请求；Session 按 session_id 自动存取历史。
运行命令：uv run python lessons/v31/01_sqlite_session_demo.py
观察重点：同一 session_id 第二轮能叫出名字；换 session_id 后不知道；item 数量不一定等于 2。
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from agents import Agent, Runner, SQLiteSession

from app.core.config import require_openai_key, settings

DB_PATH = Path(__file__).resolve().parent / ".session_demo.db"

agent = Agent(
    name="Memory Tutor",
    instructions="你是助教。用一两句中文回答，优先引用用户已经说过的信息。",
    model=settings.openai_model,
)


def print_items(label: str, items: list[object]) -> None:
    print(f"{label}_count={len(items)}")
    for index, item in enumerate(items, start=1):
        if isinstance(item, dict):
            kind = item.get("role") or item.get("type") or "dict"
        else:
            kind = type(item).__name__
        print(f"{label}_{index}={kind}")


async def main() -> None:
    require_openai_key()
    if DB_PATH.exists():
        DB_PATH.unlink()

    # SQLiteSession：SDK 官方 Session 实现。
    # 是什么：把某个 session_id 的对话条目存进 SQLite。
    # 为什么用：先不接 MySQL，只看 Runner 如何自动读写历史。
    # 什么时候：每次 Runner.run(..., session=session) 前后由 SDK 调用。
    # 参数：session_id 会话标识；db_path 默认 :memory:，这里用文件以便同一库换 id。
    # 返回：Session 对象。副作用：读写 agent_sessions / agent_messages。
    # 常见坑：每个 :memory: 实例都是独立库；要用同一个 db_path 才能证明是 session_id 在隔离。
    session = SQLiteSession("conversation_001", db_path=DB_PATH)
    first = await Runner.run(agent, "我叫小明，我喜欢 Python。", session=session)
    print(f"round1={first.final_output}")
    second = await Runner.run(agent, "我叫什么名字？我喜欢什么语言？", session=session)
    print(f"round2={second.final_output}")

    # get_items：读取该 session_id 已保存的 SDK 历史。可能含 tool/结构化条目，不只有两句文本。
    items = await session.get_items()
    print_items("history", items)

    other = SQLiteSession("conversation_002", db_path=DB_PATH)
    isolated = await Runner.run(agent, "我叫什么名字？我喜欢什么语言？", session=other)
    print(f"other_session={isolated.final_output}")
    other_items = await other.get_items()
    print_items("other_history", other_items)

    # pop_item：弹出最新一条。clear_session：清空该 session_id。单独演示，避免打断前面的两轮观察。
    popped = await session.pop_item()
    popped_kind = None
    if isinstance(popped, dict):
        popped_kind = popped.get("role") or popped.get("type")
    print(f"popped={popped_kind}")
    print(f"after_pop_count={len(await session.get_items())}")
    await session.clear_session()
    print(f"after_clear_count={len(await session.get_items())}")
    session.close()
    other.close()


if __name__ == "__main__":
    asyncio.run(main())
