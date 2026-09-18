"""用户列表：Query Model + Service。动态 where 不堆在这里。"""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from lessons.v21.app.database import get_db
from lessons.v21.app.schemas.user import UserPageResponse, UserQuery, UserResponse
from lessons.v21.app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=UserPageResponse)
def list_users(
    # Annotated[UserQuery, Query()]：把 Pydantic 模型拆成一组 Query 参数。
    # UserQuery 是请求查询条件模型，不是数据库 ORM Model。
    query: Annotated[UserQuery, Query()],
    db: DbSession,
) -> UserPageResponse:
    return user_service.list_users(db, query)


@router.get("/email-exists")
def email_exists(email: str, db: DbSession) -> dict[str, bool]:
    return {"exists": user_service.email_exists(db, email)}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DbSession) -> UserResponse:
    return UserResponse.model_validate(user_service.get(db, user_id))
