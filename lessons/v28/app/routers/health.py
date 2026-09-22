from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import check_db_health, describe_connect_error, get_db

router = APIRouter(tags=["health"])
# Annotated[AsyncSession, Depends(get_db)]：类型部分告诉 IDE/类型检查器是 AsyncSession；
# Depends(get_db) 告诉 FastAPI 当前请求如何获得 Session。
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/db")
async def health_db(db: DbSession) -> dict[str, object]:
    try:
        return await check_db_health(db)
    except Exception as extra:
        raise HTTPException(status_code=503, detail=describe_connect_error(extra)) from extra
