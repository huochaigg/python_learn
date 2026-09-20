"""多 SKU 原子扣减 + 事务。"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lessons.v24.app.database import get_db
from lessons.v24.app.schemas.order import OrderCreate, OrderResponse, OrderSummaryResponse
from lessons.v24.app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[OrderSummaryResponse])
def list_orders(db: DbSession) -> list[OrderSummaryResponse]:
    return [OrderSummaryResponse.model_validate(row) for row in order_service.list_orders(db)]


@router.post("/atomic", response_model=OrderResponse)
def create_order_atomic(body: OrderCreate, db: DbSession) -> OrderResponse:
    return OrderResponse.model_validate(order_service.create_order_atomic(db, body))
