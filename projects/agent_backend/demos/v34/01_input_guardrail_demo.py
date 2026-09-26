"""
文件作用：用阻塞式 Input Guardrail 拦住非业务问题。
实际意义：供应链助手不回答数学题；合法库存查询才会进到 Tool。
运行命令：uv run python projects/agent_backend/demos/v34/01_input_guardrail_demo.py
观察重点：数学题触发 InputGuardrailTripwireTriggered，且 tool_calls 为空；SKU002 会查库。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Agent, Runner
from agents.exceptions import InputGuardrailTripwireTriggered

from app.agents.context import AgentContext
from app.core.config import require_openai_key, settings
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)
from app.guardrails.input_guardrails import check_business_scope, classify_business_scope
from app.tools.product_tools import get_product_stock

agent = Agent[AgentContext](
    name="Guarded Stock Agent",
    instructions="你是库存助手。问 SKU 库存时必须调用 get_product_stock。用简短中文回答。",
    tools=[get_product_stock],
    input_guardrails=[check_business_scope],
    model=settings.openai_model,
)


async def run_once(message: str) -> None:
    print(f"prompt={message}")
    print(f"scope={classify_business_scope(message).model_dump()}")
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        try:
            result = await Runner.run(agent, message, context=context, max_turns=6)
            print(f"tripwire=False")
            print(f"last_agent={result.last_agent.name}")
            print(f"tool_calls={context.tool_calls}")
            print(f"answer={result.final_output}")
        except InputGuardrailTripwireTriggered as extra:
            info = extra.guardrail_result.output.output_info
            print(f"exception={type(extra).__name__}")
            print(f"tripwire=True")
            print(f"output_info={info}")
            print(f"tool_calls={context.tool_calls}")


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await run_once("帮我查询 SKU002 的库存。")
    await run_once("帮我解一道数学题。")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
