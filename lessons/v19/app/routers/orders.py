"""订单接口。业务失败全部由 Service raise，Router 不重复 catch。"""

from fastapi import APIRouter, status

from lessons.v19.app.schemas.models import OrderCreate, OrderResponse
from lessons.v19.app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/{order_id}")
def get_order(order_id: int) -> OrderResponse:
    return order_service.get_order(order_id)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_order(body: OrderCreate) -> OrderResponse:
    return order_service.create_order(body.user_id, body.sku, body.qty, body.status)
