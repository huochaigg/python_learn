"""用户业务。内存 dict 模拟数据，不接数据库。"""

from typing import Any

from lessons.v19.app.exceptions.business import UserNotFoundError


class UserService:
    def __init__(self) -> None:
        self._users: dict[int, dict[str, Any]] = {
            1: {"id": 1, "name": "Ada", "email": "ada@example.com"}
        }

    def get_user(self, user_id: int) -> dict[str, Any]:
        # Service 只 raise 业务异常，不要 raise HTTPException。
        # HTTP status / JSON 由 exception handler 映射，业务层才能脱离 FastAPI 复用。
        # 不要 except Exception: return None —— 未知错误不该被静默吞掉。
        try:
            return self._users[user_id]
        except KeyError as e:
            # raise ... from e：保留异常因果链，服务端日志能看到底层 KeyError。
            # 客户端仍然只看到统一的 UserNotFoundError JSON，不会看到 KeyError。
            raise UserNotFoundError(user_id) from e
