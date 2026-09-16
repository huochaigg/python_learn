"""订单接口：再次使用 get_pagination，证明共享 dependency。"""

from typing import Any

from fastapi import APIRouter

from lessons.v18.app.dependencies.common import PaginationDep

router = APIRouter(prefix="/orders", tags=["orders"])

_orders: list[dict[str, Any]] = [
    {"id": 1, "amount": 20},
    {"id": 2, "amount": 50},
    {"id": 3, "amount": 80},
]


@router.get("")
def list_orders(pagination: PaginationDep) -> dict[str, Any]:
    start = (pagination.page - 1) * pagination.limit
    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "items": _orders[start : start + pagination.limit],
    }
