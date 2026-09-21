from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lessons.v25.app.database import get_db
from lessons.v25.app.schemas.order import UserCreate, UserResponse
from lessons.v25.app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[UserResponse])
def list_users(db: DbSession) -> list[UserResponse]:
    return [UserResponse.model_validate(row) for row in user_service.list_users(db)]


@router.post("", response_model=UserResponse)
def create_user(body: UserCreate, db: DbSession) -> UserResponse:
    return UserResponse.model_validate(user_service.create_user(db, body))
