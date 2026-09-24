"""
文件作用：不调用大模型，演示 Pydantic Field / Literal / model_validate / model_dump。
实际意义：把 Pydantic 校验、SDK Structured Output 失败、业务库存错误区分开。
运行命令：uv run python projects/agent_backend/demos/v32/03_validation_demo.py
观察重点：stock<0、错误 type、缺字段会 ValidationError；Structured Output 正确也不等于库存事实正确。
"""

from __future__ import annotations

from pydantic import ValidationError

import _path  # noqa: F401

from app.schemas.product import ProductStockData, ProductStockResult


def show(label: str, payload: dict) -> None:
    try:
        model = ProductStockResult.model_validate(payload)
        print(f"{label}_ok={model.model_dump()}")
        print(f"{label}_json={model.model_dump_json()}")
    except ValidationError as extra:
        print(f"{label}_error={extra.error_count()}")


def main() -> None:
    show(
        "valid",
        {
            "type": "product_stock",
            "message": "可以购买",
            "data": {"sku": "SKU002", "stock": 8, "can_purchase": True},
        },
    )
    show(
        "negative_stock",
        {
            "type": "product_stock",
            "message": "坏数据",
            "data": {"sku": "SKU002", "stock": -1, "can_purchase": True},
        },
    )
    show(
        "bad_type",
        {
            "type": "order",
            "message": "不该出现的类型",
            "data": None,
        },
    )
    show("missing_message", {"type": "not_found", "data": None})
    show(
        "bad_stock_type",
        {
            "type": "product_stock",
            "message": "库存写错类型",
            "data": {"sku": "SKU002", "stock": "很多", "can_purchase": True},
        },
    )
    dumped = ProductStockData(sku="SKU003", stock=0, can_purchase=False).model_dump()
    print(f"data_dump={dumped}")
    # 业务事实：SKU999 不存在，不能用 stock=0 的合法 Schema 假装成功。
    print("business_not_found_is_not_stock_zero=True")


if __name__ == "__main__":
    main()
