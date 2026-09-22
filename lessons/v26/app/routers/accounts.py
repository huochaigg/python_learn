from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.account import Account

router = APIRouter()
DbSession = Annotated[Session, Depends(get_db)]


class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    balance: int


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "v26"}


@router.get("/accounts", response_model=list[AccountResponse])
def list_accounts(db: DbSession) -> list[Account]:
    return list(db.execute(select(Account).order_by(Account.name)).scalars().all())


@router.get("/demo/data", response_model=list[AccountResponse])
def demo_data(db: DbSession) -> list[Account]:
    return list(db.execute(select(Account).order_by(Account.name)).scalars().all())
