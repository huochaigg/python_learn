"""V7-05 继承：class Child(Parent)。

学习目标：
1. 看懂 Python 继承语法，并映射到 JS extends。
2. 确认子类能直接用父类实例方法。
3. 用 isinstance() 判断子类实例也属于父类。

运行：uv run python lessons/v7/05_inheritance.py
"""


class User:
    def __init__(self, name: str) -> None:
        self.name = name
        self.active = False

    def activate(self) -> None:
        self.active = True

    def describe(self) -> str:
        return f"User({self.name})"


# ---------------------------------------------------------------------------
# class Child(Parent)：继承。
# JS/TS 对比：class AdminUser extends User
# 子类会拿到父类的 __init__、实例方法，除非自己重写（下一课）。
# ---------------------------------------------------------------------------
class AdminUser(User):
    """管理员。本课先不写自己的 __init__，所以创建时仍然走 User.__init__。"""


admin = AdminUser("Ada")
print("admin.name =", admin.name)
admin.activate()
print("继承来的 activate 之后 active =", admin.active)
print("describe =", admin.describe())

# isinstance(obj, SomeClass)：obj 是不是这个类（或它的子类）的实例。
# 返回 bool。涉及继承时通常比 type(obj) == SomeClass 更合适。
print("isinstance(admin, AdminUser) =", isinstance(admin, AdminUser))
print("isinstance(admin, User) =", isinstance(admin, User))
print("type(admin) is User =", type(admin) is User)
print("type(admin) is AdminUser =", type(admin) is AdminUser)

if __name__ == "__main__":
    print("\n--- 05 继承 运行完毕 ---")

# 本文件重点：
# 1. class AdminUser(User) ≈ class AdminUser extends User。
# 2. 子类实例能直接调用父类方法。
# 3. isinstance(admin, User) 为 True；type(admin) is User 为 False。
# 4. 子类自己的 __init__ / 重写下一课再讲。
