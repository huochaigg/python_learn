"""订单 HTTP。Join / loading 逻辑在 Service。"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from lessons.v22.app.database import get_db
from lessons.v22.app.schemas.order import OrderCreate, OrderResponse, OrderSummaryResponse
from lessons.v22.app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=OrderResponse)
def create_order(body: OrderCreate, db: DbSession) -> OrderResponse:
    return OrderResponse.model_validate(order_service.create_order(db, body))


@router.get("", response_model=list[OrderSummaryResponse])
def list_orders(db: DbSession) -> list[OrderSummaryResponse]:
    return [OrderSummaryResponse.model_validate(row) for row in order_service.list_orders(db)]


@router.get("/with-items", response_model=list[OrderResponse])
def list_orders_with_items(db: DbSession) -> list[OrderResponse]:
    return [
        OrderResponse.model_validate(row) for row in order_service.list_orders_with_items(db)
    ]


@router.get("/by-sku", response_model=list[OrderResponse])
def find_orders_by_sku(
    db: DbSession,
    sku: Annotated[str, Query(min_length=1, max_length=32)],
) -> list[OrderResponse]:
    return [
        OrderResponse.model_validate(row) for row in order_service.find_orders_by_sku(db, sku)
    ]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: DbSession) -> OrderResponse:
    return OrderResponse.model_validate(order_service.get_order_with_items(db, order_id))
