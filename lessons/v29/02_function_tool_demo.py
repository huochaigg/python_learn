"""
文件作用：用 @function_tool 把库存查询函数交给 Agent，让模型自己决定调用。
实际意义：真实 Agent 不只是聊天，它必须调用订单、库存、物流、用户等后端能力。Function Tool 就是把已有 Python 函数暴露给 Agent 的方式。
运行命令：uv run python lessons/v29/02_function_tool_demo.py
观察重点：先出现 tool called: sku=SKU002 stock=8，再出现 final_output。不要在 Python 里手动调用 tool 再塞给 Agent。
"""

import asyncio

from agents import Agent, Runner, function_tool

from app.core.config import require_openai_key, settings

STOCK = {
    "SKU001": 100,
    "SKU002": 8,
    "SKU003": 0,
}

tool_trace: dict[str, object] = {}


@function_tool
def get_product_stock(sku: str) -> str:
    """按 SKU 查询当前库存数量。

    Args:
        sku: 商品 SKU，例如 SKU002。
    """
    # @function_tool：把普通 Python 函数注册成 LLM Tool。
    # 函数名默认变成 tool name；类型注解生成 JSON Schema；docstring 变成 tool description。
    # 参数必须清晰，否则模型填错 JSON。
    # 模型不会直接执行 Python：它只输出「我要调这个 tool + 参数」。
    # Runner 识别 Tool Call、校验参数、在本地调用这个函数，再把返回值送回 Agent Loop。
    # 因此一次 Runner.run() 内部可能：Model → Tool → Model。
    key = sku.strip().upper()
    if key not in STOCK:
        return f"没有找到 SKU={sku} 的商品"
    stock = STOCK[key]
    tool_trace["sku"] = key
    tool_trace["stock"] = stock
    print(f"tool called: sku={key} stock={stock}")
    return f"{key} 当前库存 {stock}"


agent = Agent(
    name="Stock Tool Agent",
    instructions=(
        "你是库存助手。用户问某个 SKU 库存时必须调用 get_product_stock。"
        "不要猜测数字。用简短中文回答。"
    ),
    tools=[get_product_stock],
    model=settings.openai_model,
)


async def main() -> None:
    require_openai_key()
    result = await Runner.run(agent, "SKU002 现在还有多少库存？")
    print(f"final_output: {result.final_output}")
    assert result.final_output
    assert tool_trace.get("stock") == 8


if __name__ == "__main__":
    asyncio.run(main())
