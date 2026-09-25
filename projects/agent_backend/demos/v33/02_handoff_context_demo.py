"""
文件作用：用官方 handoff() 演示 on_handoff、input_type、RunContextWrapper。
实际意义：分诊交接时记录原因，但用户身份和数据库仍来自应用层 Context。
运行命令：uv run python projects/agent_backend/demos/v33/02_handoff_context_demo.py
观察重点：handoff_reasons 来自 input_type；user_id 仍是 1，不是模型编的。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Runner
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

from app.agents.context import AgentContext
from app.agents.run_trace import last_agent_name, list_handoffs
from app.agents.triage_agent import triage_agent
from app.core.config import require_openai_key
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)


async def run_once(message: str) -> None:
    # handoff(..., on_handoff=..., input_type=HandoffData)
    # input_type：交接 Tool 的 Pydantic 参数。模型生成 reason，SDK 校验后再交给 on_handoff。
    # 它不替代下一位 Agent 的用户输入，也不替代 ctx.context.user_id / db。
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        result = await Runner.run(triage_agent, message, context=context, max_turns=8)
        print(f"prompt={message}")
        print(f"last_agent={last_agent_name(result)}")
        print(f"handoffs={list_handoffs(result)}")
        print(f"handoff_reasons={context.handoff_reasons}")
        print(f"context_user_id={context.user_id}")
        print(f"answer={result.final_output}")


async def main() -> None:
    require_openai_key()
    print(f"recommended_prompt_prefix_chars={len(RECOMMENDED_PROMPT_PREFIX)}")
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await run_once("SKU002 还有多少库存？")
    await run_once("订单 ORD001 现在是什么状态？")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
