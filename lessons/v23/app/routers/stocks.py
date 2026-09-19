"""库存查看。给事务前后对照用。"""

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lessons.v23.app.database import get_db
from lessons.v23.app.schemas.order import StockResponse
from lessons.v23.app.services import order_service

router = APIRouter(prefix="/stocks", tags=["stocks"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[StockResponse])
def list_stocks(db: DbSession) -> list[StockResponse]:
    return [StockResponse.model_validate(row) for row in order_service.list_stocks(db)]
