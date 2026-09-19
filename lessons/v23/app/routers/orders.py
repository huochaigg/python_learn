"""订单 HTTP。commit/rollback 不写在 Router。"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lessons.v23.app.database import get_db
from lessons.v23.app.schemas.order import OrderCreate, OrderResponse, OrderSummaryResponse
from lessons.v23.app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=OrderResponse)
def create_order(body: OrderCreate, db: DbSession) -> OrderResponse:
    return OrderResponse.model_validate(order_service.create_order(db, body))


@router.get("", response_model=list[OrderSummaryResponse])
def list_orders(db: DbSession) -> list[OrderSummaryResponse]:
    return [OrderSummaryResponse.model_validate(row) for row in order_service.list_orders(db)]
