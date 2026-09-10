"""V7-09 综合练习：User、AdminUser、activate、super、__str__、isinstance。

学习目标：
1. 自己写一遍基础类、继承和 super()。
2. 用实例方法改状态，用 isinstance 判断类型。
3. 先 TODO，再对照示例答案。

运行：uv run python lessons/v7/09_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""


# =============================================================================
# 练习 1
# TODO: 定义 User，__init__(name, age)，实例属性 name/age/active=False。
#       再写 activate(self) -> None。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.active = False

    def activate(self) -> None:
        self.active = True

    def __str__(self) -> str:
        status = "active" if self.active else "inactive"
        return f"User({self.name}, {self.age}, {status})"


tom = User("Tom", 31)
print("创建后 active =", tom.active)
tom.activate()
print("activate 后 =", tom.active)


# =============================================================================
# 练习 2
# TODO: AdminUser(User)，__init__ 增加 permissions: list[str]。
#       必须 super().__init__(name, age)。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


class AdminUser(User):
    def __init__(self, name: str, age: int, permissions: list[str]) -> None:
        super().__init__(name, age)
        self.permissions = permissions

    def __str__(self) -> str:
        return f"AdminUser({self.name}, perms={self.permissions})"


ada = AdminUser("Ada", 30, ["users:write"])
print("ada.name / age 来自父类 =", ada.name, ada.age)
print("ada.permissions =", ada.permissions)
ada.activate()
print("继承来的 activate 后 active =", ada.active)


# =============================================================================
# 练习 3
# TODO: print(tom) 和 print(ada)，确认走了各自的 __str__。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")
print(tom)
print(ada)


# =============================================================================
# 练习 4
# TODO: 用 isinstance 判断 ada 是否同时属于 AdminUser 和 User；
#       对比 type(ada) is User。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")
print("isinstance(ada, AdminUser) =", isinstance(ada, AdminUser))
print("isinstance(ada, User) =", isinstance(ada, User))
print("type(ada) is User =", type(ada) is User)


# =============================================================================
# 练习 5
# TODO: 写 describe(obj: User) -> str，根据是否 AdminUser 打印不同摘要。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")


def describe(obj: User) -> str:
    if isinstance(obj, AdminUser):
        return f"admin {obj.name} {obj.permissions}"
    return f"user {obj.name}"


print(describe(tom))
print(describe(ada))

if __name__ == "__main__":
    print("\n--- 09 综合练习 运行完毕 ---")

# 本文件重点：
# 1. User() 创建实例，没有 new。
# 2. 子类 __init__ 要 super().__init__(...)。
# 3. activate 改的是当前实例的 active。
# 4. isinstance 能识别继承；type(...) is Parent 不能。
# 5. __str__ 让 print 可读。
