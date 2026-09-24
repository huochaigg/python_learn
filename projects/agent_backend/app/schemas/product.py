from typing import Literal

from pydantic import BaseModel, Field


class ProductAnalysis(BaseModel):
    """Demo / Agent 输出模型：SKU 库存分析。

    output_type 会把这个 BaseModel 转成 JSON Schema 交给模型；
    Runner 结束时用 Pydantic 校验并得到 Python 对象，不必自己 json.loads。
    """

    sku: str = Field(min_length=1, description="商品 SKU")
    stock: int = Field(ge=0, description="当前库存，不能为负数")
    can_purchase: bool = Field(description="仅表示库存是否大于 0，不是下单许可")
    message: str = Field(min_length=1, description="给用户看的简短说明")


class ProductStockData(BaseModel):
    sku: str = Field(min_length=1)
    stock: int = Field(ge=0)
    can_purchase: bool


ProductResultType = Literal["product_stock", "not_found", "text"]


class ProductStockResult(BaseModel):
    """Agent.output_type：模型最终必须产出的结构。

    Tool 返回的是可信库存字符串；本模型是 Agent 组织后的最终输出。
    二者不是一回事。商品不存在时 type=not_found，data=None，禁止用 stock=0 表示错误。
    """

    type: ProductResultType
    message: str = Field(min_length=1)
    data: ProductStockData | None = None


class ProductAnalyzeRequest(BaseModel):
    conversation_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class ProductAnalyzeResponse(BaseModel):
    """FastAPI response_model：HTTP 返回给前端的 DTO。

    可以和 Agent.output_type 形状相近，但不是同一个对象。
    Service 会用数据库再算一遍 can_purchase，不把模型数字当成下单依据。
    """

    conversation_id: str
    type: ProductResultType
    message: str
    data: ProductStockData | None = None
