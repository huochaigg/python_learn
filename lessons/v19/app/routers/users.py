"""用户接口。薄 Router：调 Service，不包一层 try/except BizException。"""

from fastapi import APIRouter

from lessons.v19.app.schemas.models import UserResponse
from lessons.v19.app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}")
def get_user(user_id: int) -> UserResponse:
    # 查不到时 Service raise UserNotFoundError，交给全局 BizException handler。
    return user_service.get_user(user_id)
