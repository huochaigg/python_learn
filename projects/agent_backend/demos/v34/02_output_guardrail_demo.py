"""
文件作用：用 Output Guardrail 检查最终结果，而不是 HTTP response_model。
实际意义：库存分析对象生成后，再拦负数库存和内部测试标记。
运行命令：uv run python projects/agent_backend/demos/v34/02_output_guardrail_demo.py
观察重点：stock=-1 和 INTERNAL_TEST 会 tripwire=True；合法 ProductAnalysis 放行。
"""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

import _path  # noqa: F401

from agents import Agent, RunContextWrapper

from app.agents.context import AgentContext
from app.guardrails.output_guardrails import evaluate_final_output, inspect_final_output
from app.schemas.product import ProductAnalysis

dummy_agent = Agent(name="Output Check Agent", instructions="output check")


def check(label: str, output: object) -> None:
    ctx = RunContextWrapper(context=AgentContext(db=MagicMock(), user_id=1))
    inspected = inspect_final_output(output)
    result = evaluate_final_output(ctx, dummy_agent, output)
    print(f"case={label}")
    print(f"inspect={inspected.model_dump()}")
    print(f"tripwire={result.tripwire_triggered}")
    print(f"output_info={result.output_info}")


async def main() -> None:
    check(
        "valid",
        ProductAnalysis(sku="SKU002", stock=8, can_purchase=True, message="可买"),
    )
    check("negative_stock", {"sku": "SKU002", "stock": -1, "message": "坏数据"})
    check(
        "internal_marker",
        ProductAnalysis(
            sku="SKU002",
            stock=8,
            can_purchase=True,
            message="INTERNAL_TEST 不要给用户看",
        ),
    )


if __name__ == "__main__":
    asyncio.run(main())
