from pathlib import Path

import pytest
from agents import Agent, Runner
from agents.memory import SQLiteSession
from agents.testing import ScriptedModel, assistant_message

pytestmark = pytest.mark.asyncio


def _memory_agent(text: str, name: str = "Memory Agent") -> Agent:
    return Agent(name=name, instructions="简短回答。", model=ScriptedModel([[assistant_message(text)]]))


async def test_same_session_keeps_history() -> None:
    # 这个测试做什么：同一 session_id 第一轮写入的信息，第二轮仍能从 Session 读到。
    # 输入：两轮 Runner.run 共用 SQLiteSession。内部：不连 MySQL，使用 SDK 官方 SQLiteSession。
    # 返回：第一轮 items 含「张三」；第二轮 items 更长，且能跑出脚本答案。
    # 为什么这样写：测的是 Session 读写隔离与历史拼接，不是模型是否「记住」。
    # 常见坑：每个单测都连真实 MySQL 又慢又脆；MySQL 留给 integration test。
    session = SQLiteSession("session_same", db_path=":memory:")
    first = await Runner.run(_memory_agent("ok"), "请记住：我的名字是张三。", session=session)
    assert first.final_output == "ok"
    first_items = await session.get_items()
    assert "张三" in str(first_items)
    second = await Runner.run(_memory_agent("你叫张三"), "我叫什么名字？", session=session)
    assert second.final_output == "你叫张三"
    second_items = await session.get_items()
    assert len(second_items) > len(first_items)
    assert "我叫什么名字" in str(second_items) or "我叫什么名字？" in str(second_items)


async def test_sessions_do_not_read_each_other(tmp_path: Path) -> None:
    # 隔离：同一 SQLite 文件里 session_A / session_B 不能互相读到对方的历史。
    db_path = str(tmp_path / "agent_sessions.db")
    session_a = SQLiteSession("session_A", db_path=db_path)
    session_b = SQLiteSession("session_B", db_path=db_path)
    await Runner.run(
        _memory_agent("收到A"),
        "SECRET_TOKEN_SESSION_A",
        session=session_a,
    )
    items_a = await session_a.get_items()
    items_b = await session_b.get_items()
    assert "SECRET_TOKEN_SESSION_A" in str(items_a)
    assert items_b == []
    await Runner.run(_memory_agent("收到B"), "SESSION_B_ONLY", session=session_b)
    items_b = await session_b.get_items()
    assert "SESSION_B_ONLY" in str(items_b)
    assert "SECRET_TOKEN_SESSION_A" not in str(items_b)
    assert "SESSION_B_ONLY" not in str(await session_a.get_items())
