"""
文件作用：演示 Guardrail、max_turns、Tool 超时等 SDK 异常，以及应用层错误码映射。
实际意义：Service 把 SDK 异常转成安全的 HTTP/SSE 错误，不把堆栈发给用户。
运行命令：uv run python projects/agent_backend/demos/v34/04_agent_error_demo.py
观察重点：数学题异常类型是 InputGuardrailTripwireTriggered；慢工具超时报 ToolTimeoutError。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from unittest.mock import MagicMock

from agents import Agent, Runner, function_tool
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    MaxTurnsExceeded,
    ModelBehaviorError,
    ModelTimeoutError,
    OutputGuardrailTripwireTriggered,
    ToolTimeoutError,
)

from app.agents.context import AgentContext
from app.core.agent_exceptions import map_sdk_exception
from app.core.config import require_openai_key, settings
from app.core.database import AsyncSessionLocal, engine, init_schema, migrate_schema, seed_products
from app.guardrails.input_guardrails import check_business_scope


@function_tool(timeout=0.05, timeout_behavior="raise_exception")
async def slow_lookup(ctx: object, sku: str) -> str:
    # timeout / timeout_behavior：限制单次 Tool 调用时长。
    # raise_exception → ToolTimeoutError，中断 Run。
    # error_as_result → 超时字符串作为 Tool Result 交给模型，Run 继续。
    # 超时不撤销外部副作用。本函数只有 asyncio.sleep，没有写库。
    _ = ctx
    _ = sku
    await asyncio.sleep(1)
    return "should not finish"


@function_tool(timeout=0.05, timeout_behavior="error_as_result")
async def slow_lookup_as_result(ctx: object, sku: str) -> str:
    _ = ctx
    _ = sku
    await asyncio.sleep(1)
    return "should not finish"


def show_mapping(exc: BaseException) -> None:
    mapped = map_sdk_exception(exc)
    print(f"sdk={type(exc).__name__}")
    print(f"app_code={mapped.code}")
    print(f"http={mapped.status_code}")
    print(f"public={mapped.message}")


async def run_input_block() -> None:
    agent = Agent(
        name="Blocked Agent",
        instructions="只回答库存。",
        input_guardrails=[check_business_scope],
        model=settings.openai_model,
    )
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        try:
            await Runner.run(agent, "帮我解一道数学题。", context=context, max_turns=3)
            print("unexpected_success=true")
        except InputGuardrailTripwireTriggered as extra:
            print(f"prompt=帮我解一道数学题。")
            print(f"exception={type(extra).__name__}")
            show_mapping(extra)


async def run_timeout() -> None:
    agent = Agent(
        name="Timeout Agent",
        instructions="必须调用 slow_lookup，参数 sku=SKU002。",
        tools=[slow_lookup],
        model=settings.openai_model,
    )
    try:
        await Runner.run(agent, "查询 SKU002", max_turns=4)
        print("timeout_unexpected_success=true")
    except ToolTimeoutError as extra:
        print(f"exception={type(extra).__name__}")
        print(f"tool_name={extra.tool_name}")
        show_mapping(extra)
    except Exception as extra:
        print(f"exception={type(extra).__name__}")
        show_mapping(extra)


async def run_timeout_as_result() -> None:
    agent = Agent(
        name="Timeout Result Agent",
        instructions="必须调用 slow_lookup_as_result，参数 sku=SKU002。然后用一句话说明工具结果。",
        tools=[slow_lookup_as_result],
        model=settings.openai_model,
    )
    result = await Runner.run(agent, "查询 SKU002", max_turns=4)
    print(f"timeout_behavior=error_as_result")
    print(f"last_agent={result.last_agent.name}")
    print(f"answer={result.final_output}")


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    print("map_max_turns")
    show_mapping(MaxTurnsExceeded("too many turns"))
    print("map_model_behavior")
    show_mapping(ModelBehaviorError("bad json"))
    print("map_output_guardrail")
    dummy_result = MagicMock()
    dummy_result.guardrail = MagicMock()
    show_mapping(OutputGuardrailTripwireTriggered(dummy_result))
    print("map_model_timeout")
    show_mapping(ModelTimeoutError(1.5))
    await run_input_block()
    await run_timeout()
    await run_timeout_as_result()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
