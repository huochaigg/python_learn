from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from lessons.v25.app.database import get_db
from lessons.v25.app.schemas.order import OrderCreate, OrderResponse
from lessons.v25.app.services import order_service

router = APIRouter(prefix="/orders", tags=["orders"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[OrderResponse])
def list_orders(db: DbSession) -> list[OrderResponse]:
    return [OrderResponse.model_validate(row) for row in order_service.list_orders(db)]


@router.get("/by-key/{idempotency_key}", response_model=OrderResponse)
def get_order_by_key(idempotency_key: str, db: DbSession) -> OrderResponse:
    return OrderResponse.model_validate(order_service.get_by_key(db, idempotency_key))


@router.post("", response_model=OrderResponse)
def create_order(
    body: OrderCreate,
    db: DbSession,
    # Header Idempotency-Key：客户端重试必须带同一个 key。
    # 缺失由 FastAPI 校验成 422。不要服务端随机生成，否则每次重试都是新 key，幂等失效。
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=1)],
) -> OrderResponse:
    return OrderResponse.model_validate(
        order_service.create_order_idempotent(db, idempotency_key, body)
    )
