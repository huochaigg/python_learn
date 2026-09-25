"""
文件作用：用 Agent(handoffs=[...]) 做最简单的真实 Handoff。
实际意义：供应链分诊把库存问题交给库存专家，把订单问题交给订单专家。
运行命令：uv run python projects/agent_backend/demos/v33/01_handoff_basic_demo.py
观察重点：SKU002 的 last_agent 是 Inventory Agent；ORD001 的 last_agent 是 Order Agent。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Agent, Runner
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from app.agents.context import AgentContext
from app.agents.inventory_agent import inventory_agent
from app.agents.order_agent import order_agent
from app.agents.run_trace import last_agent_name, list_handoffs, list_tool_names
from app.core.config import require_openai_key, settings
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)

# Agent.handoffs：声明当前 Agent 可以把本轮交给谁。
# 是什么：交给 SDK 的交接目标列表。Runner 把每个目标变成 transfer_to_*。
# 为什么用：让模型自己选专家，而不是 Python if/else 手动 Runner.run 另一个 Agent。
# 什么时候：Triage 判断当前用户问题属于库存或订单时。
# 参数：Agent 实例或 handoff() 返回值。本 Demo 用最简形式传入 Agent。
# 返回值：无。交接发生在 Runner 内部；结束后看 result.last_agent / new_items。
# 副作用：当前轮次由目标 Agent 接管并生成最终回答。不开关数据库 Session。
# 常见坑：Handoff 看起来像 Tool，但 Tool Result 不会回到原 Agent 继续说；控制权已经走了。
# 对应：LangGraph 把 state 切到另一个 node；不是普通 Function Tool，也不是 if sku: inventory().
basic_triage = Agent[AgentContext](
    name="Triage Agent",
    instructions=prompt_with_handoff_instructions(
        "你是供应链分诊助手。库存/SKU 问题必须交给 Inventory Agent。"
        "订单号/订单状态必须交给 Order Agent。不要自己编造库存或订单。"
    ),
    handoffs=[inventory_agent, order_agent],
    model=settings.openai_model,
)


async def run_once(message: str) -> None:
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        result = await Runner.run(basic_triage, message, context=context, max_turns=8)
    print(f"prompt={message}")
    print(f"last_agent={last_agent_name(result)}")
    print(f"handoffs={list_handoffs(result)}")
    print(f"tools={list_tool_names(result)}")
    print(f"answer={result.final_output}")


async def observe_stream(message: str) -> None:
    # agent_updated_stream_event：当前负责的 Agent 变了。
    # run_item_stream_event + handoff_*_item：交接记录。不要和文本 delta 混成一种消息。
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        streamed = Runner.run_streamed(basic_triage, message, context=context, max_turns=8)
        async for event in streamed.stream_events():
            event_type = getattr(event, "type", "")
            if event_type == "agent_updated_stream_event":
                print(f"stream_event=agent_updated_stream_event agent={event.new_agent.name}")
            elif event_type == "run_item_stream_event":
                item_type = getattr(event.item, "type", "")
                if item_type in {"handoff_call_item", "handoff_output_item"}:
                    print(f"stream_event=run_item_stream_event item={item_type}")
        print(f"stream_last_agent={last_agent_name(streamed)}")
        print(f"stream_answer={streamed.final_output}")


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await run_once("SKU002 还有多少库存？")
    await run_once("订单 ORD001 现在是什么状态？")
    await observe_stream("SKU002 还有多少库存？")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
