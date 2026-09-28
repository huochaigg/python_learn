"""
文件作用：演示什么时候才需要 custom_span()。
实际意义：Runner 已经自动追踪 Agent / Generation / Function Tool / Guardrail / Handoff。
只有业务上额外想观察、且 SDK 不会自动包起来的步骤，才值得手写一个 Span。
运行命令：uv run python projects/agent_backend/demos/v35/05_custom_span_demo.py
观察重点：inventory_business_check 是自定义业务步骤；get_product_stock 仍然走 SDK 自动 Function Span，不要重复包一层。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Runner, custom_span, flush_traces, gen_trace_id, get_current_trace, trace

from app.agents.context import AgentContext
from app.agents.product_agent import product_agent
from app.core.config import require_openai_key, settings
from app.core.database import (
    AsyncSessionLocal,
    engine,
    init_schema,
    migrate_schema,
    seed_orders,
    seed_products,
)
from app.repositories.product_repository import product_repository
from app.core.tracing import traces_dashboard_hint


async def inventory_business_check(sku: str) -> dict[str, object]:
    # 这个方法做什么：在 Agent Run 之外做一次「可售检查」。
    # 输入：sku。内部：查库、判断 stock>0。返回：给排查用的摘要，不是 Trace 数据库。
    # 为什么 custom_span：这段 Python 业务处理不是 Function Tool，SDK 不会自动打 Span。
    # 适合 custom_span 的例子：复杂订单计算、自定义 RAG、外部 API、多步数据库处理。
    # 不适合：再包一层已经是 Function Tool 的 get_product_stock。
    # 常见坑：Span data 不要放密码 / Token / 完整敏感库存明细。
    with custom_span("inventory_business_check", data={"sku": sku}):
        async with AsyncSessionLocal() as session:
            product = await product_repository.get_by_sku(session, sku)
            if product is None:
                return {"sku": sku, "found": False, "can_sell": False}
            return {
                "sku": product.sku,
                "found": True,
                "can_sell": product.stock > 0,
            }


async def main() -> None:
    require_openai_key()
    if not settings.openai_tracing_api_key:
        print("缺少 OPENAI_TRACING_API_KEY，Trace 不会出现在 platform.openai.com")
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    sku = "SKU002"
    with trace(
        "inventory-custom-span-workflow",
        trace_id=gen_trace_id(),
        group_id="conversation_custom_001",
        metadata={"agent_name": product_agent.name, "environment": "demo"},
    ):
        current = get_current_trace()
        trace_id = None if current is None else current.trace_id
        print(f"trace_id={trace_id}")
        print(f"group_id=conversation_custom_001")
        check = await inventory_business_check(sku)
        print(f"custom_span=inventory_business_check")
        print(f"business_check={check}")
        async with AsyncSessionLocal() as session:
            context = AgentContext(db=session, user_id=1)
            result = await Runner.run(
                product_agent,
                f"{sku} 还有多少库存？",
                context=context,
                max_turns=6,
            )
        print(f"auto_traced_tool_calls={context.tool_calls}")
        print(f"answer={result.final_output}")
        print(f"dashboard={traces_dashboard_hint(trace_id)}")
    print("sdk_auto_spans=Agent,Generation,FunctionTool")
    print("custom_span_only_for_extra_business_steps=True")
    flush_traces()
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
