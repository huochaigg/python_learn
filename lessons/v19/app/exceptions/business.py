"""具体业务异常。子类可以共用 BizException handler，不必每个都单独注册。"""

from lessons.v19.app.exceptions.base import BizException


class UserNotFoundError(BizException):
    """用户不存在。对应 HTTP 404。"""

    def __init__(self, user_id: int) -> None:
        super().__init__(
            f"user not found: {user_id}",
            code="USER_NOT_FOUND",
            status_code=404,
        )


class OrderNotFoundError(BizException):
    """订单不存在。对应 HTTP 404。"""

    def __init__(self, order_id: int) -> None:
        super().__init__(
            f"order not found: {order_id}",
            code="ORDER_NOT_FOUND",
            status_code=404,
        )


class InsufficientStockError(BizException):
    """库存不足。对应 HTTP 409 Conflict。本课会给它单独注册一个更具体的 handler 做对比。"""

    def __init__(self, sku: str, left: int, need: int) -> None:
        super().__init__(
            f"sku={sku} left={left} need={need}",
            code="INSUFFICIENT_STOCK",
            status_code=409,
        )
        self.sku = sku
        self.left = left
        self.need = need


class InvalidOrderStatusError(BizException):
    """当前状态不允许该操作。对应 HTTP 400。"""

    def __init__(self, current: str, *, action: str) -> None:
        super().__init__(
            f"cannot {action} when status={current}",
            code="INVALID_ORDER_STATUS",
            status_code=400,
        )
