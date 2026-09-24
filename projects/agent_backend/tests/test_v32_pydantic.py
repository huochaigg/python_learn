from pydantic import ValidationError

from app.schemas.product import ProductAnalysis, ProductStockData, ProductStockResult


def test_product_analysis_valid_type() -> None:
    model = ProductAnalysis.model_validate(
        {"sku": "SKU001", "stock": 100, "can_purchase": True, "message": "可买"}
    )
    assert isinstance(model, ProductAnalysis)
    assert model.model_dump()["stock"] == 100


def test_stock_cannot_be_negative() -> None:
    try:
        ProductStockData.model_validate({"sku": "SKU002", "stock": -1, "can_purchase": False})
    except ValidationError as extra:
        assert extra.error_count() >= 1
        return
    raise AssertionError("expected ValidationError")


def test_literal_type_rejected() -> None:
    try:
        ProductStockResult.model_validate(
            {"type": "order", "message": "x", "data": None}
        )
    except ValidationError as extra:
        assert extra.error_count() >= 1
        return
    raise AssertionError("expected ValidationError")


def test_missing_required_field() -> None:
    try:
        ProductStockResult.model_validate({"type": "not_found", "data": None})
    except ValidationError as extra:
        assert extra.error_count() >= 1
        return
    raise AssertionError("expected ValidationError")


def test_model_dump_json() -> None:
    model = ProductStockResult(
        type="not_found",
        message="没有这个商品",
        data=None,
    )
    text = model.model_dump_json()
    assert "not_found" in text
    assert "没有这个商品" in text
