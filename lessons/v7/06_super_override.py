"""V7-06 super() 与方法重写。

学习目标：
1. 子类 __init__ 里用 super().__init__() 先跑父类初始化。
2. 会重写父类方法。
3. 知道忘了 super() 时，父类属性可能根本没挂上。

运行：uv run python lessons/v7/06_super_override.py
"""


class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.active = True

    def describe(self) -> str:
        return f"{self.name}, {self.age}"


class AdminUser(User):
    def __init__(self, name: str, age: int, permissions: list[str]) -> None:
        # super()：拿到父类实现，再调用它的方法。
        # 用途：子类补自己的字段前，先让父类把 name/age 初始化完。
        # JS/TS 对比：super(name, age) / super().__init__ 这一类。
        # 注意：本课不深入 MRO。先记住「去调用父类那份」。
        # 坑：子类写了 __init__ 就不会自动跑父类 __init__，必须自己 super()。
        super().__init__(name, age)
        self.permissions = permissions

    def describe(self) -> str:
        # 重写 override：子类定义与父类同名的方法，调用时优先用子类版本。
        # JS/TS 对比：同样是同名方法覆盖；Python 不必写 override 关键字。
        return f"admin {self.name} perms={self.permissions}"

    def describe_with_parent(self) -> str:
        return super().describe() + " [admin]"


admin = AdminUser("Ada", 30, ["users:write", "users:read"])
print("admin.name / age 来自父类初始化 =", admin.name, admin.age)
print("admin.permissions 来自子类 =", admin.permissions)
print("重写后的 describe =", admin.describe())
print("需要时仍可 super().describe() =", admin.describe_with_parent())

user = User("Tom", 31)
print("父类实例仍用父类 describe =", user.describe())

if __name__ == "__main__":
    print("\n--- 06 super / override 运行完毕 ---")

# 本文件重点：
# 1. 子类自己写了 __init__，就要记得 super().__init__(...)。
# 2. super() 用来访问父类实现，类似 JS super。
# 3. 同名方法就是重写；实例调用时走子类版本。
# 4. 还想用父类逻辑时，在子类方法里再 super().xxx()。
