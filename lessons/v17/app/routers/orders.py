"""订单接口。独立 Router + Schema，业务保持最简。"""

from typing import Any

from fastapi import APIRouter, status

from lessons.v17.app.schemas.order import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["orders"])

_orders: dict[int, dict[str, Any]] = {
    1: {"id": 1, "user_id": 1, "amount": 99, "status": "pending"}
}
_next_id = 2


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate) -> dict[str, Any]:
    global _next_id
    saved = {
        "id": _next_id,
        "user_id": order.user_id,
        "amount": order.amount,
        "status": "pending",
    }
    _orders[_next_id] = saved
    _next_id += 1
    return saved


@router.get("")
def list_orders() -> list[OrderResponse]:
    return list(_orders.values())


@router.get("/{order_id}")
def get_order(order_id: int) -> OrderResponse:
    order = _orders.get(order_id)
    if order is None:
        # TODO: 后续异常处理版本改成 HTTPException(status_code=404)
        return OrderResponse(
            id=order_id, user_id=0, amount=0, status="cancelled"
        )
    return order
