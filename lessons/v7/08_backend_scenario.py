"""V7-08 后端小场景：User / AdminUser / UserService。

学习目标：
1. 用 class 模拟一层业务对象 + 一个 Service。
2. 综合 __init__、实例属性、实例方法、继承、super()。
3. 仍然只是内存里的 list，不碰数据库和 FastAPI。

运行：uv run python lessons/v7/08_backend_scenario.py
"""


class User:
    def __init__(self, user_id: int, name: str, age: int) -> None:
        self.id = user_id
        self.name = name
        self.age = age
        self.active = True

    def deactivate(self) -> None:
        self.active = False

    def __str__(self) -> str:
        return f"User({self.id}, {self.name})"


class AdminUser(User):
    def __init__(self, user_id: int, name: str, age: int, permissions: list[str]) -> None:
        super().__init__(user_id, name, age)
        self.permissions = permissions

    def __str__(self) -> str:
        return f"AdminUser({self.id}, {self.name}, perms={self.permissions})"


class UserNotFoundError(Exception):
    """用户不存在。"""


class UserService:
    """内存版用户服务，形态接近 NestJS/FastAPI 的 Service。"""

    def __init__(self) -> None:
        self._users: list[User] = []
        self._next_id = 1

    def create_user(self, name: str, age: int) -> User:
        user = User(self._next_id, name, age)
        self._next_id += 1
        self._users.append(user)
        return user

    def create_admin(self, name: str, age: int, permissions: list[str]) -> AdminUser:
        admin = AdminUser(self._next_id, name, age, permissions)
        self._next_id += 1
        self._users.append(admin)
        return admin

    def get_user(self, user_id: int) -> User:
        for user in self._users:
            if user.id == user_id:
                return user
        raise UserNotFoundError(f"user not found: {user_id}")


service = UserService()
tom = service.create_user("Tom", 31)
ada = service.create_admin("Ada", 30, ["users:write"])
print("create_user ->", tom)
print("create_admin ->", ada)
print("get_user(1) ->", service.get_user(1))
print("isinstance(ada, User) =", isinstance(ada, User))

tom.deactivate()
print("deactivate 之后 tom.active =", tom.active)

try:
    service.get_user(99)
except UserNotFoundError as e:
    print("get 不到就 raise =", e)

if __name__ == "__main__":
    print("\n--- 08 后端场景 运行完毕 ---")

# 本文件重点：
# 1. User / AdminUser 是领域对象；UserService 持有列表并提供 create/get。
# 2. 找不到就 raise，而不是返回 None。
# 3. _users 用单下划线表示内部状态。
# 4. 这就是后面 FastAPI Service 的缩影，只是还没有真正的 DB。
