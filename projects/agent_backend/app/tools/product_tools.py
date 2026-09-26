import logging

from agents import RunContextWrapper, function_tool

from ..agents.context import AgentContext
from ..guardrails.tool_guardrails import check_sku_tool_input, check_tool_output_secrets
from ..repositories.product_repository import product_repository

logger = logging.getLogger(__name__)


@function_tool(
    tool_input_guardrails=[check_sku_tool_input],
    tool_output_guardrails=[check_tool_output_secrets],
)
async def get_product_stock(ctx: RunContextWrapper[AgentContext], sku: str) -> str:
    """按 SKU 查询商品当前库存。

    Args:
        sku: 商品 SKU，例如 SKU001。
    """
    # Tool Input Guardrail 在本函数之前执行；非法 SKU 不会进到这里。
    # Tool Output Guardrail 在本函数返回之后执行，不能撤销已经发生的查询。
    # 权限/库存事实仍由 Repository 决定，不靠 Guardrail 或 Prompt。
    ctx.context.tool_calls.append(f"get_product_stock:{sku.strip().upper()}")
    try:
        product = await product_repository.get_by_sku(ctx.context.db, sku.strip().upper())
    except Exception:
        logger.exception("get_product_stock failed sku=%s", sku)
        raise
    if product is None:
        return f"没有找到 SKU={sku} 的商品"
    print(f"tool called: sku={product.sku} stock={product.stock}")
    return f"{product.sku} 当前库存 {product.stock}"
