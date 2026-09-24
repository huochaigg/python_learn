"""
文件作用：用 Agent(output_type=ProductAnalysis) 得到真正的 Pydantic 对象。
实际意义：前端卡片需要稳定字段，不能只拿一段自由文本再自己 json.loads。
运行命令：uv run python projects/agent_backend/demos/v32/01_structured_output_demo.py
观察重点：final_output 的 Python 类型是 ProductAnalysis，不是 str。
"""

from __future__ import annotations

import asyncio

import _path  # noqa: F401

from agents import Agent, Runner

from app.core.config import require_openai_key, settings
from app.core.model_settings import structured_output_model_settings
from app.schemas.product import ProductAnalysis

_schema = ProductAnalysis.model_json_schema()

# output_type：把 Pydantic 模型编成 JSON Schema 交给模型，结束时校验并解析。
# 优先 BaseModel：Field 约束、JSON Schema、FastAPI 都能直接用。
# TypedDict / dataclass 也能当输出类型，但校验和文档不如 BaseModel 完整。
# 常见坑：不要自己 json.loads(result.final_output)；也不要把流式 delta 当完整 JSON。
# 兼容网关不支持 json_schema 时，用 json_object + 本地 output_type 校验。
agent = Agent(
    name="Product Analysis Agent",
    instructions=(
        "根据用户给出的 SKU 和库存数字，输出 ProductAnalysis JSON。"
        "can_purchase 仅当 stock>0 为 true。用一句中文填写 message。"
        "不要编造用户没给的数字。"
        f"JSON Schema: {_schema}"
    ),
    output_type=ProductAnalysis,
    model=settings.openai_model,
    model_settings=structured_output_model_settings(),
)


async def main() -> None:
    require_openai_key()
    result = await Runner.run(agent, "SKU001 库存 100，请分析能否购买。")
    output = result.final_output
    print(f"type={type(output).__name__}")
    if isinstance(output, ProductAnalysis):
        print(f"sku={output.sku}")
        print(f"stock={output.stock}")
        print(f"can_purchase={output.can_purchase}")
        print(f"message={output.message}")
        print(output.model_dump_json())
    else:
        print(f"final_output={output!r}")


if __name__ == "__main__":
    asyncio.run(main())
