from agents import Agent
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from ..core.config import settings
from ..tools.product_tools import get_product_stock
from .context import AgentContext

# Inventory Agent：Handoff 接管当前轮次后，由它调用既有库存 Tool 并生成最终回答。
# 复用 get_product_stock / ProductRepository，不另写一套库存查询。
# 没有反向 handoffs，避免和 Triage 无限互相交接。
inventory_agent = Agent[AgentContext](
    name="Inventory Agent",
    instructions=prompt_with_handoff_instructions(
        "你是库存专家。用户问 SKU/库存时必须调用 get_product_stock，不要编造数字。"
        "找不到商品就明确说没有。不处理下单、扣库存。用简短中文回答。"
    ),
    tools=[get_product_stock],
    model=settings.openai_model,
)
