"""用户业务。Service 负责规则，Repository 只负责存取。"""

from collections.abc import Callable

from lessons.v15.order_app.exceptions import UserNotFoundError
from lessons.v15.order_app.models.user import Role, User, UserId
from lessons.v15.order_app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, users: UserRepository) -> None:
        # constructor 注入 Repository：调用方把依赖传进来，而不是在类内部 new。
        # 思想和后面 FastAPI Depends / NestJS constructor injection 相近。
        # 本版本没有 DI 框架，main 里手动组装即可。
        self._users = users

    async def create_user(self, name: str, role: Role, *, active: bool = True) -> User:
        return await self._users.create(User(id=0, name=name, role=role, active=active))

    async def get_user(self, user_id: UserId) -> User:
        user = await self._users.get_by_id(user_id)
        if user is None:
            raise UserNotFoundError(f"user not found: {user_id}")
        return user

    async def list_users(self) -> list[User]:
        return await self._users.list_all()

    def active_names(self, users: list[User]) -> list[str]:
        # 列表推导式：过滤 active 用户并取出名字。数据已在内存，不必 async for。
        return [user.name for user in users if user.active]

    def filter_users(self, users: list[User], predicate: Callable[[User], bool]) -> list[User]:
        # Callable[[User], bool]：收一个 User、返回 bool 的函数。TS：(u: User) => boolean
        return [user for user in users if predicate(user)]
