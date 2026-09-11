"""V10-10 后端 typing 小场景：TypedDict + Literal + 别名 + Generic + Callable。

学习目标：
1. 用类型把「输入 dict、角色、过滤器、统一响应」串起来。
2. 看清类型如何逐步描述真实后端数据结构。
3. 仍然只是内存 Demo，不引入 FastAPI / Pydantic / 数据库。

运行：uv run python lessons/v10/10_backend_scenario.py
"""

from typing import Callable, Generic, Literal, TypeVar, TypedDict

type UserId = int
Role = Literal["admin", "user"]
T = TypeVar("T")


class UserIn(TypedDict):
    name: str
    role: Role


class UserOut(TypedDict):
    id: UserId
    name: str
    role: Role
    active: bool


class ApiResponse(Generic[T]):
    def __init__(self, data: T, ok: bool = True) -> None:
        self.data = data
        self.ok = ok

    def __repr__(self) -> str:
        return f"ApiResponse(ok={self.ok}, data={self.data!r})"


class UserService:
    def __init__(self) -> None:
        self._users: list[UserOut] = []
        self._next_id: UserId = 1

    def create_user(self, payload: UserIn) -> ApiResponse[UserOut]:
        user: UserOut = {
            "id": self._next_id,
            "name": payload["name"],
            "role": payload["role"],
            "active": True,
        }
        self._next_id += 1
        self._users.append(user)
        return ApiResponse(user)

    def list_users(
        self,
        predicate: Callable[[UserOut], bool] | None = None,
    ) -> ApiResponse[list[UserOut]]:
        items = self._users
        if predicate is not None:
            items = [user for user in items if predicate(user)]
        return ApiResponse(items)


def is_admin(user: UserOut) -> bool:
    return user["role"] == "admin"


service = UserService()
print(service.create_user({"name": "Tom", "role": "user"}))
print(service.create_user({"name": "Ada", "role": "admin"}))
print("all =", service.list_users())
print("admins =", service.list_users(is_admin))

if __name__ == "__main__":
    print("\n--- 10 后端场景 运行完毕 ---")

# 本文件重点：
# 1. TypedDict 描述入参/出参 dict；Literal 锁住 role。
# 2. UserId 别名让 id 的含义比裸 int 清楚。
# 3. ApiResponse[T] 统一包一层 data。
# 4. Callable 描述过滤器；| None = None 才表示可以不传。
