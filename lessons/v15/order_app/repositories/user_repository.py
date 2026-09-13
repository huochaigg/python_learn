"""用户数据访问。只存取，不决定「找不到算不算错」。"""

from lessons.v15.order_app.models.user import User, UserId
from lessons.v15.order_app.repositories.session import FakeDatabaseSession


class UserRepository:
    def __init__(self) -> None:
        self._store: dict[UserId, User] = {}
        self._next_id = 0

    async def create(self, user: User) -> User:
        self._next_id += 1
        saved = User(id=self._next_id, name=user.name, role=user.role, active=user.active)
        self._store[saved.id] = saved
        return saved

    async def get_by_id(self, user_id: UserId) -> User | None:
        # 返回 User | None：Repository 允许查不到。
        # Service 再决定是继续返回 None，还是 raise UserNotFoundError。
        return self._store.get(user_id)

    async def list_all(self) -> list[User]:
        # 部分查询走 Async Context Manager，复习 V14：进入/退出都可以 await。
        async with FakeDatabaseSession("users") as _session:
            return list(self._store.values())

    async def update(self, user: User) -> User:
        self._store[user.id] = user
        return user
