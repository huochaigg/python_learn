"""
文件作用：两个 session_id 并行对话，验证历史隔离。
实际意义：session_id 是会话标识，不等于 user_id；一个用户可以有多个 Conversation。
运行命令：uv run python lessons/v31/03_session_isolation_demo.py
观察重点：会话 A 只记得 SCM，会话 B 只记得 Agent；两边 item 互不影响。
"""

from __future__ import annotations

import asyncio

from agents import Agent, Runner
from agents.extensions.memory import SQLAlchemySession

from app.core.config import require_openai_key, settings
from app.core.database import engine
from app.sessions.agent_session import init_sdk_session_tables

agent = Agent(
    name="Memory Tutor",
    instructions="你是助教。用一两句中文回答，只根据当前会话历史判断项目名称。",
    model=settings.openai_model,
)


async def run_pair(session_id: str, first: str, second: str) -> tuple[str, str, int]:
    session = SQLAlchemySession(
        session_id,
        engine=engine,
        create_tables=False,
        ensure_ascii=False,
    )
    await session.clear_session()
    round1 = await Runner.run(agent, first, session=session)
    round2 = await Runner.run(agent, second, session=session)
    return str(round1.final_output), str(round2.final_output), len(await session.get_items())


async def main() -> None:
    require_openai_key()
    await init_sdk_session_tables()
    a1, a2, a_count = await run_pair("v31_iso_a", "我的项目叫 SCM。", "我的项目叫什么？")
    b1, b2, b_count = await run_pair("v31_iso_b", "我的项目叫 Agent。", "我的项目叫什么？")
    print(f"session_a_round1={a1}")
    print(f"session_a_round2={a2}")
    print(f"session_a_items={a_count}")
    print(f"session_b_round1={b1}")
    print(f"session_b_round2={b2}")
    print(f"session_b_items={b_count}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
