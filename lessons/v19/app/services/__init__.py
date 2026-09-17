"""Service 包：只描述业务规则和业务异常，不拼 HTTP JSON。"""

from lessons.v19.app.services.order_service import OrderService
from lessons.v19.app.services.user_service import UserService

user_service = UserService()
order_service = OrderService(user_service)

__all__ = ["OrderService", "UserService", "order_service", "user_service"]
