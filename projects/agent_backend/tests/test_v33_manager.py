import os

import pytest
from agents import Runner

from app.agents.context import AgentContext
from app.agents.manager_agent import manager_agent
from app.agents.run_trace import last_agent_name, list_handoffs, list_tool_names
from app.core.config import settings
from app.core.database import (
    AsyncSessionLocal,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)


pytestmark = pytest.mark.asyncio


def _has_key() -> bool:
    return bool(settings.openai_api_key or os.getenv("OPENAI_API_KEY"))


async def test_manager_calls_expert_tools() -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        result = await Runner.run(
            manager_agent,
            "帮我查 SKU002 库存，再看订单 ORD001 状态，最后总结一下。",
            context=context,
            max_turns=8,
        )
    assert last_agent_name(result) == "Manager Agent"
    assert list_handoffs(result) == []
    tools = list_tool_names(result)
    assert "ask_inventory_expert" in tools
    assert "ask_order_expert" in tools
    assert context.user_id == 1
    assert result.final_output
