import logging

from agents import Agent, RunContextWrapper, handoff
from agents.extensions.handoff_prompt import prompt_with_handoff_instructions

from ..core.config import settings
from ..schemas.handoff import HandoffData
from .context import AgentContext
from .inventory_agent import inventory_agent
from .order_agent import order_agent

logger = logging.getLogger(__name__)


async def on_inventory_handoff(
    ctx: RunContextWrapper[AgentContext], data: HandoffData
) -> None:
    # on_handoff：模型选定交接目标并生成 input_type JSON 后、目标 Agent 开始前执行。
    # RunContextWrapper.context：应用层本轮依赖（db / user_id）。可信，不来自模型。
    # input_type 数据：模型生成的交接元数据。只记录原因，不能当鉴权。
    ctx.context.handoff_reasons.append(f"inventory:{data.reason}")
    logger.info("handoff to Inventory Agent reason=%s", data.reason)


async def on_order_handoff(
    ctx: RunContextWrapper[AgentContext], data: HandoffData
) -> None:
    ctx.context.handoff_reasons.append(f"order:{data.reason}")
    logger.info("handoff to Order Agent reason=%s", data.reason)


# handoff()：把目标 Agent 包装成交接 Tool（transfer_to_*）。
# 提供 input_type 时必须同时给 on_handoff，否则 SDK 抛 UserError。
# prompt_with_handoff_instructions：给 instructions 加上 RECOMMENDED_PROMPT_PREFIX。
# 它只是告诉模型如何使用 transfer_to_*，不是权限系统，也不是强制业务规则。
#
# 应用层策略：每个 HTTP 请求都从 Triage Agent 起步。
# result.last_agent 只描述本轮最终回答者；SDK Session 不会自动选用下一轮入口 Agent。
# Input Guardrail 只在链首 Agent 运行。本对象不挂 Guardrail，以免改变 /agent/multi/chat。
triage_agent = Agent[AgentContext](
    name="Triage Agent",
    instructions=prompt_with_handoff_instructions(
        "你是供应链分诊助手。库存/SKU 问题必须交给 Inventory Agent。"
        "订单号/订单状态必须交给 Order Agent。"
        "不要自己编造库存或订单。不要处理下单或取消订单。"
        "闲聊可以自己简短回答。"
    ),
    handoffs=[
        handoff(
            inventory_agent,
            on_handoff=on_inventory_handoff,
            input_type=HandoffData,
        ),
        handoff(
            order_agent,
            on_handoff=on_order_handoff,
            input_type=HandoffData,
        ),
    ],
    model=settings.openai_model,
)
