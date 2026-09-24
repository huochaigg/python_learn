from agents import Agent

from ..core.config import settings
from ..tools.product_tools import get_product_stock
from .context import AgentContext

# Agent[AgentContext]：泛型标明本 Agent 运行时 Local Context 的类型。
# 类似 TypeScript 的 Agent<AgentContext>。这是类型约定，不会把 Context 自动发给模型。
#
# Agent 本身是可复用的行为配置（name / instructions / tools / model），
# 类似「一组 prompt + 能力声明」，不是一次 HTTP 调用。
# AsyncSession 绝不能写进这个模块级对象；每次 Runner.run(context=...) 再传入。
product_agent = Agent[AgentContext](
    name="Product Stock Agent",
    instructions=(
        "你是电商库存助手。用户询问某个 SKU 的库存时，必须调用 get_product_stock。"
        "不要编造库存数字。也可以根据对话历史回答用户之前说过的内容。"
        "用简短中文回答。"
    ),
    tools=[get_product_stock],
    model=settings.openai_model,
)
