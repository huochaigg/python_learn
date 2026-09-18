"""用户 HTTP 接口。ORM 查询放 Service。"""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from lessons.v20.app.database import get_db
from lessons.v20.app.schemas.user import UserCreate, UserResponse, UserUpdate
from lessons.v20.app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

# Annotated[Session, Depends(get_db)]：
# Session 给类型检查器；Depends(get_db) 告诉 FastAPI 每个请求 yield 一个新 Session。
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, db: DbSession) -> UserResponse:
    return user_service.create(db, body)


@router.get("", response_model=list[UserResponse])
def list_users(db: DbSession) -> list[UserResponse]:
    return user_service.list_all(db)


@router.get("/by-email/{email}", response_model=UserResponse | None)
def get_user_by_email(email: str, db: DbSession) -> UserResponse | None:
    return user_service.get_by_email(db, email)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession) -> UserResponse:
    return user_service.get(db, user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(user_id: int, body: UserUpdate, db: DbSession) -> UserResponse:
    return user_service.update(db, user_id, body)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DbSession) -> None:
    user_service.delete(db, user_id)
