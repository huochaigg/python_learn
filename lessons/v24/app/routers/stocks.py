"""库存 HTTP。atomic-deduct 适合 SQLite 学习；pessimistic 仅教学 API。"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lessons.v24.app.database import get_db
from lessons.v24.app.schemas.order import DeductRequest, StockResponse
from lessons.v24.app.services import order_service

router = APIRouter(prefix="/stocks", tags=["stocks"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[StockResponse])
def list_stocks(db: DbSession) -> list[StockResponse]:
    return [StockResponse.model_validate(row) for row in order_service.list_stocks(db)]


@router.get("/{sku}", response_model=StockResponse)
def get_stock(sku: str, db: DbSession) -> StockResponse:
    return StockResponse.model_validate(order_service.get_stock(db, sku))


@router.post("/{sku}/atomic-deduct", response_model=StockResponse)
def atomic_deduct(sku: str, body: DeductRequest, db: DbSession) -> StockResponse:
    return StockResponse.model_validate(order_service.deduct_atomic(db, sku, body.quantity))


@router.post("/{sku}/pessimistic-deduct", response_model=StockResponse)
def pessimistic_deduct(sku: str, body: DeductRequest, db: DbSession) -> StockResponse:
    """教学/实验：发出 SELECT FOR UPDATE。不声称 SQLite 能还原 MySQL/PostgreSQL 行锁等待。"""
    return StockResponse.model_validate(
        order_service.deduct_pessimistic_demo(db, sku, body.quantity)
    )
