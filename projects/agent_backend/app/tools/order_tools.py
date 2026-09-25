import logging

from agents import RunContextWrapper, function_tool

from ..agents.context import AgentContext
from ..repositories.order_repository import order_repository

logger = logging.getLogger(__name__)


@function_tool
async def get_order_status(ctx: RunContextWrapper[AgentContext], order_no: str) -> str:
    """按订单号查询当前用户的订单状态。只读，不创建、不取消、不扣库存。

    Args:
        order_no: 订单号，例如 ORD001。
    """
    # 授权在 Tool 内做：user_id 来自 AgentContext，不是模型参数，也不能靠 HandoffData。
    # 找不到和无权查看返回不同文案，避免把别人的订单状态泄漏出去。
    user_id = ctx.context.user_id
    if user_id is None:
        return "缺少用户身份，无法查询订单"
    try:
        order = await order_repository.get_owned(
            ctx.context.db, order_no.strip().upper(), user_id
        )
    except Exception:
        logger.exception("get_order_status failed order_no=%s", order_no)
        raise
    if order is None:
        existing = await order_repository.get_by_order_no(ctx.context.db, order_no.strip().upper())
        if existing is not None:
            return f"无权查看订单 {order_no}"
        return f"没有找到订单 {order_no}"
    print(f"tool called: order={order.order_no} status={order.status}")
    return f"{order.order_no} 状态={order.status} sku={order.sku}"
