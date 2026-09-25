from agents import Agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from ..core.config import settings
from ..tools.order_tools import get_order_status
from .context import AgentContext

# Order Agent：最小只读订单专家。不创建、不取消、不扣库存。
# 授权仍在 Tool 内用 AgentContext.user_id 判断，不靠模型决定能否绕过。
order_agent = Agent[AgentContext](
    name="Order Agent",
    instructions=prompt_with_handoff_instructions(
        "你是订单查询专家。必须调用 get_order_status，不要编造订单状态。"
        "只读查询。用户要求创建、取消订单或扣库存时，明确说暂不支持。"
        "找不到或无权查看时如实说明。用简短中文回答。"
    ),
    tools=[get_order_status],
    model=settings.openai_model,
)
