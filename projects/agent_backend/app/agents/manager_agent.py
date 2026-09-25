from agents import Agent

from ..core.config import settings
from .context import AgentContext
from .inventory_agent import inventory_agent
from .order_agent import order_agent

# Agent.as_tool()：把专家 Agent 变成 FunctionTool。
# 是什么：嵌套 Runner，专家拿到模型生成的 input，跑完把结果字符串返回 Manager。
# 为什么用：Manager 要汇总库存+订单，不能把控制权交出去。
# 什么时候：Manager 判断需要子任务时调用 ask_*_expert。
# 参数：tool_name / tool_description / max_turns；默认入参是 {input: str}。
# 返回值：FunctionTool。嵌套 Agent 的 final_output 变成 Tool Result。
# 副作用：会再跑一轮专家 Agent，共用同一 AgentContext，不另开 HTTP。
# 常见坑：不要当成 Handoff。Handoff 会换 last_agent；as_tool 后 last_agent 仍是 Manager。
# 对应：LangGraph 的 subgraph 当 node tool 调用，不是把整个图切到另一个 agent。
manager_agent = Agent[AgentContext](
    name="Manager Agent",
    instructions=(
        "你是供应链经理。库存问题调用 ask_inventory_expert，订单问题调用 ask_order_expert。"
        "可以先后调用多个专家，然后用中文做简短总结。不要编造库存或订单。"
        "用户要求下单、取消或扣库存时，明确说暂不支持。"
    ),
    tools=[
        inventory_agent.as_tool(
            "ask_inventory_expert",
            "查询商品 SKU 库存。把用户的库存问题原样传给专家。",
            max_turns=4,
        ),
        order_agent.as_tool(
            "ask_order_expert",
            "查询订单状态。把用户的订单问题原样传给专家。",
            max_turns=4,
        ),
    ],
    model=settings.openai_model,
)
