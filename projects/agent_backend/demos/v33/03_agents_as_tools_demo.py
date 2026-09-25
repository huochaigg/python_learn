"""
文件作用：用 Agent.as_tool() 让 Manager 调用库存专家和订单专家。
实际意义：经理保留控制权，专家只做子任务，最后由 Manager 统一总结。
运行命令：uv run python projects/agent_backend/demos/v33/03_agents_as_tools_demo.py
观察重点：last_agent 仍是 Manager Agent；tools 里会出现 ask_inventory_expert / ask_order_expert。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Runner

from app.agents.context import AgentContext
from app.agents.manager_agent import manager_agent
from app.agents.run_trace import last_agent_name, list_handoffs, list_tool_names
from app.core.config import require_openai_key
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    message = "帮我查 SKU002 库存，再看订单 ORD001 状态，最后总结一下。"
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        result = await Runner.run(manager_agent, message, context=context, max_turns=8)
    print(f"prompt={message}")
    print(f"last_agent={last_agent_name(result)}")
    print(f"handoffs={list_handoffs(result)}")
    print(f"tools={list_tool_names(result)}")
    print(f"context={context}")
    print(f"answer={result.final_output}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
