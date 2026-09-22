from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import check_db_health, describe_connect_error, get_db

router = APIRouter(tags=["health"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/db")
def health_db(db: DbSession) -> dict[str, object]:
    try:
        return check_db_health(db)
    except Exception as extra:
        raise HTTPException(status_code=503, detail=describe_connect_error(extra)) from extra
