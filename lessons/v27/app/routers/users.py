from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserCreate, UserResponse
from ..services import user_service
from ..services.user_service import DuplicateEmailError

router = APIRouter(prefix="/users", tags=["users"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=UserResponse)
def create_user(body: UserCreate, db: DbSession) -> UserResponse:
    try:
        user = user_service.create_user(db, body)
    except DuplicateEmailError as extra:
        raise HTTPException(status_code=409, detail=f"email already exists: {extra.email}") from extra
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def list_users(db: DbSession) -> list[UserResponse]:
    return [UserResponse.model_validate(row) for row in user_service.list_users(db)]


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession) -> UserResponse:
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return UserResponse.model_validate(user)
