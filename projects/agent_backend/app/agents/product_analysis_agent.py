from agents import Agent

from ..core.config import settings
from ..core.model_settings import structured_output_model_settings
from ..schemas.product import ProductStockResult
from ..tools.product_tools import get_product_stock
from .context import AgentContext

_schema = ProductStockResult.model_json_schema()

# output_type=ProductStockResult：模型最终输出必须符合该 Pydantic 模型。
# Tool 结果不是 final_output。不要对 SSE delta 做完整 JSON 校验。
product_analysis_agent = Agent[AgentContext](
    name="Product Analysis Agent",
    instructions=(
        "你是库存分析助手。用户问某个 SKU 的库存或能否购买时，必须调用 get_product_stock。"
        "不要编造库存数字。"
        "最终只输出一个 JSON 对象，符合 ProductStockResult："
        "商品存在时 type=product_stock，data.sku/stock 来自 Tool，can_purchase 仅当 stock>0。"
        "商品不存在时 type=not_found，data 必须为 null，禁止用 stock=0 表示找不到。"
        "普通闲聊时 type=text，data 为 null。"
        "can_purchase 只表示库存是否大于 0，不是最终下单许可。"
        f"JSON Schema: {_schema}"
    ),
    tools=[get_product_stock],
    output_type=ProductStockResult,
    model=settings.openai_model,
    model_settings=structured_output_model_settings(),
)
