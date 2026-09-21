from lessons.v25.app.services.order_service import OrderService, create_order_idempotent
from lessons.v25.app.services.user_service import UserService, email_exists

order_service = OrderService()
user_service = UserService()

__all__ = [
    "OrderService",
    "UserService",
    "create_order_idempotent",
    "email_exists",
    "order_service",
    "user_service",
]
