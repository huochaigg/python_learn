"""
文件作用：演示 Tool Input/Output Guardrail 的 allow、reject_content、raise_exception。
实际意义：非法 SKU 在查库前被拒；含密钥的 Tool 输出不能回到模型。
运行命令：uv run python projects/agent_backend/demos/v34/03_tool_guardrail_demo.py
观察重点：?? 不会打印 tool called；密钥输出 behavior=raise_exception。Output Guardrail 不能撤销已执行的查询。
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

import _path  # noqa: F401

from agents import Agent, Runner
from agents.tool_context import ToolContext
from agents.tool_guardrails import ToolInputGuardrailData, ToolOutputGuardrailData

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
from app.guardrails.tool_guardrails import (
    evaluate_sku_tool_input,
    evaluate_tool_output_secrets,
    inspect_sku,
    inspect_tool_output_text,
)
from app.tools.product_tools import get_product_stock

dummy_agent = Agent(name="Tool Guard Agent", instructions="tool guard")


def fake_input(sku: str) -> ToolInputGuardrailData:
    context = ToolContext(
        context=AgentContext(db=MagicMock(), user_id=1),
        tool_name="get_product_stock",
        tool_call_id="call_1",
        tool_arguments=f'{{"sku":"{sku}"}}',
        tool_input={"sku": sku},
    )
    return ToolInputGuardrailData(context=context, agent=dummy_agent)


def fake_output(text: str) -> ToolOutputGuardrailData:
    context = ToolContext(
        context=AgentContext(db=MagicMock(), user_id=1),
        tool_name="get_product_stock",
        tool_call_id="call_2",
        tool_arguments='{"sku":"SKU002"}',
        tool_input={"sku": "SKU002"},
    )
    return ToolOutputGuardrailData(context=context, agent=dummy_agent, output=text)


def show_behavior(label: str, output: object) -> None:
    behavior = getattr(output, "behavior", output)
    kind = behavior.get("type") if isinstance(behavior, dict) else getattr(behavior, "type", behavior)
    print(f"case={label}")
    print(f"behavior={kind}")
    print(f"output_info={getattr(output, 'output_info', None)}")


async def run_stock_query(message: str) -> None:
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        result = await Runner.run(
            Agent[AgentContext](
                name="Stock Agent",
                instructions="问库存必须调用 get_product_stock。用简短中文回答。",
                tools=[get_product_stock],
                model=settings.openai_model,
            ),
            message,
            context=context,
            max_turns=6,
        )
        print(f"prompt={message}")
        print(f"tool_calls={context.tool_calls}")
        print(f"answer={result.final_output}")


async def main() -> None:
    show_behavior("sku_ok", evaluate_sku_tool_input(fake_input("SKU002")))
    show_behavior("sku_empty", evaluate_sku_tool_input(fake_input("")))
    show_behavior("sku_bad", evaluate_sku_tool_input(fake_input("??")))
    print(f"inspect_sku={inspect_sku('??').model_dump()}")
    show_behavior(
        "output_ok",
        evaluate_tool_output_secrets(fake_output("SKU002 当前库存 8")),
    )
    show_behavior(
        "output_secret",
        evaluate_tool_output_secrets(fake_output("mysql+asyncmy://root:secret@127.0.0.1/db")),
    )
    print(f"inspect_secret={inspect_tool_output_text('password=abc').model_dump()}")
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await run_stock_query("帮我查询 SKU002 的库存。")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
