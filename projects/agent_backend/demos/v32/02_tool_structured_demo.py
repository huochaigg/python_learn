"""
文件作用：先真实查询 MySQL 库存 Tool，再产出结构化 ProductStockResult。
实际意义：Tool 给可信数据，Agent 组织最终输出；二者不是同一个对象。
运行命令：uv run python projects/agent_backend/demos/v32/02_tool_structured_demo.py
观察重点：SKU002 的 stock 来自数据库；不存在的 SKU 是 not_found，不是 stock=0。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Runner

from app.agents.context import AgentContext
from app.agents.product_analysis_agent import product_analysis_agent
from app.core.config import require_openai_key
from app.core.database import AsyncSessionLocal, engine, init_schema, migrate_schema, seed_products
from app.schemas.product import ProductStockResult


async def run_once(message: str) -> None:
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session)
        result = await Runner.run(product_analysis_agent, message, context=context)
    output = result.final_output
    print(f"prompt={message}")
    print(f"type={type(output).__name__}")
    if isinstance(output, ProductStockResult):
        print(output.model_dump_json())
    else:
        print(f"final_output={output!r}")


async def main() -> None:
    require_openai_key()
    await init_schema()
    await migrate_schema()
    await seed_products()
    await run_once("SKU002 还有多少库存？能不能购买？")
    await run_once("SKU999 还有多少库存？")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
