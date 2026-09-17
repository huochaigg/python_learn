"""订单业务。库存也在内存里。"""

from typing import Any

from lessons.v19.app.exceptions.business import (
    InsufficientStockError,
    InvalidOrderStatusError,
    OrderNotFoundError,
)
from lessons.v19.app.services.user_service import UserService


class OrderService:
    def __init__(self, users: UserService) -> None:
        self._users = users
        self._orders: dict[int, dict[str, Any]] = {
            1: {"id": 1, "user_id": 1, "sku": "sku-1", "qty": 1, "status": "pending"}
        }
        self._stock = {"sku-1": 10, "sku-2": 2}
        self._next_id = 2

    def get_order(self, order_id: int) -> dict[str, Any]:
        try:
            return self._orders[order_id]
        except KeyError as e:
            raise OrderNotFoundError(order_id) from e

    def create_order(
        self, user_id: int, sku: str, qty: int, status: str = "pending"
    ) -> dict[str, Any]:
        self._users.get_user(user_id)
        if status != "pending":
            raise InvalidOrderStatusError(status, action="create")
        left = self._stock.get(sku, 0)
        if qty > left:
            raise InsufficientStockError(sku, left, qty)
        self._stock[sku] = left - qty
        saved = {
            "id": self._next_id,
            "user_id": user_id,
            "sku": sku,
            "qty": qty,
            "status": "pending",
        }
        self._orders[self._next_id] = saved
        self._next_id += 1
        return saved
