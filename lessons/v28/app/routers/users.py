from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.user import UserCreate, UserResponse, UserUpdate
from ..services import user_service
from ..services.user_service import DuplicateEmailError

router = APIRouter(prefix="/users", tags=["users"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("", response_model=UserResponse)
async def create_user(body: UserCreate, db: DbSession) -> UserResponse:
    try:
        user = await user_service.create_user(db, body)
    except DuplicateEmailError as extra:
        raise HTTPException(status_code=409, detail=f"email already exists: {extra.email}") from extra
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
async def list_users(db: DbSession) -> list[UserResponse]:
    rows = await user_service.list_users(db)
    return [UserResponse.model_validate(row) for row in rows]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: DbSession) -> UserResponse:
    user = await user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse.model_validate(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, body: UserUpdate, db: DbSession) -> UserResponse:
    user = await user_service.update_user(db, user_id, body)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse.model_validate(user)


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: DbSession) -> dict[str, bool]:
    deleted = await user_service.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="user not found")
    return {"deleted": True}
