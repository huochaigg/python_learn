"""
文件作用：用官方 trace() 包一次真实 Agent Run，观察 workflow / trace_id / group_id / metadata。
实际意义：真实 Agent Run 可能经历 模型生成 → Tool 调用 → Tool 返回 → Handoff → Guardrail → 再次生成。
只靠 print 很难串起完整链路。Tracing 把一次工作流记下来，步骤之间有父子关系和耗时。
运行命令：uv run python projects/agent_backend/demos/v35/04_tracing_demo.py
观察重点：两次 Run 的 group_id 都是 conversation_001。若配置了 OPENAI_BASE_URL，trace_id 可能显示 no-op（不上报 Dashboard），但 group_id / metadata 概念仍然成立。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Runner, gen_trace_id, get_current_trace, trace

from app.agents.context import AgentContext
from app.agents.product_agent import product_agent
from app.core.config import require_openai_key
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)
from app.core.tracing import agent_trace_metadata

# conversation_id：业务会话 ID。本 Demo 用它当 group_id。
# session_id：SDK 历史上下文标识（本 Demo 不传 Session，避免和 Trace 概念混在一起）。
# trace_id：这一次 workflow / Run 的追踪 ID。
# group_id：把同一会话的多次 Trace 归成一组，方便排查「这个对话前后发生了什么」。
CONVERSATION_ID = "conversation_001"


async def run_once(label: str, message: str) -> str | None:
    # trace() 必须当 context manager 用：进入时 start，离开时 finish。
    # 即使 Runner 抛异常，__exit__ 也会结束 Trace，失败请求同样能被看到。
    # 不要每个 Tool 手写 Span；Runner.run 默认已经会打 Agent / Generation / Function Tool 等 Span。
    workflow_name = "inventory-agent-workflow"
    metadata = agent_trace_metadata(
        user_id=1,
        conversation_id=CONVERSATION_ID,
        agent_name=product_agent.name,
        environment="demo",
    )
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session, user_id=1)
        with trace(
            workflow_name,
            trace_id=gen_trace_id(),
            group_id=CONVERSATION_ID,
            metadata=metadata,
        ):
            current = get_current_trace()
            print(f"label={label}")
            print(f"workflow_name={workflow_name}")
            print(f"trace_id={None if current is None else current.trace_id}")
            print(f"group_id={CONVERSATION_ID}")
            print(f"metadata={metadata}")
            result = await Runner.run(product_agent, message, context=context, max_turns=6)
            print(f"tool_calls={context.tool_calls}")
            print(f"answer={result.final_output}")
            return None if current is None else current.trace_id


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    first_id = await run_once("first_run", "SKU002 还有多少库存？")
    second_id = await run_once("second_run", "SKU001 呢？")
    print("same_group_id=conversation_001")
    print(f"first_trace_id={first_id}")
    print(f"second_trace_id={second_id}")
    print("note=OPENAI_BASE_URL 时 set_tracing_disabled(True)，trace_id 可能是 no-op；group_id 仍然是 conversation_id")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
