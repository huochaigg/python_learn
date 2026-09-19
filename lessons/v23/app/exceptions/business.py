from lessons.v23.app.exceptions.base import BizException


class InvalidOrderError(BizException):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="INVALID_ORDER", status_code=400)


class InsufficientStockError(BizException):
    def __init__(self, sku: str, left: int, need: int) -> None:
        super().__init__(
            f"sku={sku} left={left} need={need}",
            code="INSUFFICIENT_STOCK",
            status_code=409,
        )
        self.sku = sku
        self.left = left
        self.need = need


class StockNotFoundError(BizException):
    def __init__(self, sku: str) -> None:
        super().__init__(
            f"stock not found: {sku}",
            code="STOCK_NOT_FOUND",
            status_code=404,
        )
        self.sku = sku


class DuplicateOrderNoError(BizException):
    def __init__(self, order_no: str) -> None:
        super().__init__(
            f"duplicate order_no: {order_no}",
            code="DUPLICATE_ORDER_NO",
            status_code=409,
        )
        self.order_no = order_no
