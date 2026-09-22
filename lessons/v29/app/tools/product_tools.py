import logging

from agents import RunContextWrapper, function_tool

from ..agents.context import AgentContext
from ..repositories.product_repository import product_repository

logger = logging.getLogger(__name__)


@function_tool
async def get_product_stock(ctx: RunContextWrapper[AgentContext], sku: str) -> str:
    """按 SKU 查询商品当前库存。

    Args:
        sku: 商品 SKU，例如 SKU001。
    """
    # RunContextWrapper：SDK 注入的运行期包装。ctx.context 才是我们传入的 AgentContext。
    # db 来自当前 HTTP Request 的 get_db()，不是全局 Session。
    # Runner.run() 必须在该 Session 仍然存活时跑完，否则 Tool 访问已关闭 Session。
    try:
        product = await product_repository.get_by_sku(ctx.context.db, sku.strip().upper())
    except Exception:
        logger.exception("get_product_stock failed sku=%s", sku)
        raise
    if product is None:
        return f"没有找到 SKU={sku} 的商品"
    print(f"tool called: sku={product.sku} stock={product.stock}")
    return f"{product.sku} 当前库存 {product.stock}"
