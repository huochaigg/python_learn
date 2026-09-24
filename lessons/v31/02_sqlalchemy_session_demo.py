"""
文件作用：用官方 SQLAlchemySession 把历史写入真实 MySQL，并重建 Session 对象再读。
实际意义：进程重启后只要 session_id 和数据库还在，模型上下文就能恢复。
运行命令：uv run python lessons/v31/02_sqlalchemy_session_demo.py
观察重点：同一 session_id 第二轮记得爱好；新 Python 对象仍能读到；agent_messages 表有记录。
"""

from __future__ import annotations

import asyncio

from sqlalchemy import text

from agents import Agent, Runner
from agents.extensions.memory import SQLAlchemySession

from app.core.config import require_openai_key, settings
from app.core.database import engine
from app.sessions.agent_session import init_sdk_session_tables

SESSION_ID = "v31_sqlalchemy_demo"

agent = Agent(
    name="Memory Tutor",
    instructions="你是助教。用一两句中文回答，优先引用用户已经说过的信息。",
    model=settings.openai_model,
)


async def mysql_item_count(session_id: str) -> int:
    async with engine.connect() as connection:
        result = await connection.execute(
            text("SELECT COUNT(*) FROM agent_messages WHERE session_id = :sid"),
            {"sid": session_id},
        )
        return int(result.scalar() or 0)


async def main() -> None:
    require_openai_key()
    # SQLAlchemySession：官方 MySQL/Postgres/SQLite 历史后端。
    # 是什么：按 session_id 把 SDK item JSON 存进 agent_messages。
    # 为什么用：复用现有 mysql+asyncmy AsyncEngine，不必另起同步 pymysql。
    # 什么时候：Runner.run(session=...) 时 SDK 先 get_items 再在结束后 add_items。
    # 参数：session_id、engine=AsyncEngine。返回 Session 对象，历史不绑在该对象上。
    # 副作用：自己开事务写 SDK 表，和业务 AsyncSession 不共享事务。
    # 常见坑：MySQL 上不要用 create_tables=True（VARCHAR 无长度）；先跑兼容 DDL。
    #         不要把同一份历史再手动拼进 Runner input。
    await init_sdk_session_tables()
    session = SQLAlchemySession(
        SESSION_ID,
        engine=engine,
        create_tables=False,
        ensure_ascii=False,
    )
    first = await Runner.run(agent, "我最喜欢的编程语言是 Python。", session=session)
    print(f"round1={first.final_output}")
    second = await Runner.run(agent, "我刚才说最喜欢什么？", session=session)
    print(f"round2={second.final_output}")
    print(f"same_object_items={len(await session.get_items())}")
    session2 = SQLAlchemySession(
        SESSION_ID,
        engine=engine,
        create_tables=False,
        ensure_ascii=False,
    )
    third = await Runner.run(agent, "我之前说过什么？", session=session2)
    print(f"rebuilt_object={third.final_output}")
    print(f"rebuilt_items={len(await session2.get_items())}")
    print(f"mysql_agent_messages={await mysql_item_count(SESSION_ID)}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
