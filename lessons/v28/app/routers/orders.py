from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.order import OrderCreate, OrderResponse
from ..services import order_service
from ..services.order_service import DuplicateOrderNoError

router = APIRouter(prefix="/orders", tags=["orders"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("", response_model=OrderResponse)
async def create_order(body: OrderCreate, db: DbSession) -> OrderResponse:
    try:
        order = await order_service.create_order(db, body)
    except DuplicateOrderNoError as extra:
        raise HTTPException(status_code=409, detail=f"order_no already exists: {extra.order_no}") from extra
    return OrderResponse.model_validate(order)


@router.get("", response_model=list[OrderResponse])
async def list_orders(db: DbSession) -> list[OrderResponse]:
    rows = await order_service.list_orders(db)
    return [OrderResponse.model_validate(row) for row in rows]


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: DbSession) -> OrderResponse:
    order = await order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return OrderResponse.model_validate(order)
