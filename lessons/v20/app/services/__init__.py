"""Service 包。"""

from lessons.v20.app.services.user_service import UserService

user_service = UserService()

__all__ = ["UserService", "user_service"]
