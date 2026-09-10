"""V7-07 dunder 方法与 isinstance。

学习目标：
1. 知道 __init__ / __str__ 这类双下划线方法叫 dunder method。
2. 会写 __str__，让 print(obj) 可读。
3. 继承场景优先 isinstance()，而不是 type(x) == X。

运行：uv run python lessons/v7/07_dunder_isinstance.py
"""


class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    def __str__(self) -> str:
        # __str__：对象转成「给人看的字符串」时用。
        # 用途：print(user)、str(user) 会走到这里。
        # JS/TS 对比：≈ toString()
        # dunder method：double underscore，Python 对象协议的一部分。
        # 本课只碰 __init__ / __str__，其他魔术方法先不展开。
        return f"User(name={self.name!r}, age={self.age})"


class AdminUser(User):
    def __str__(self) -> str:
        return f"AdminUser({self.name})"


tom = User("Tom", 31)
admin = AdminUser("Ada", 30)

print("print(tom) ->", tom)
print("str(admin) ->", str(admin))
print("没定义 __str__ 时，默认会是类似 <__main__.User object at 0x...>")

print("type(tom) =", type(tom))
print("type(admin) =", type(admin))
print("type(admin) is User =", type(admin) is User)
print("isinstance(admin, User) =", isinstance(admin, User))
print("isinstance(admin, AdminUser) =", isinstance(admin, AdminUser))
print("isinstance(tom, AdminUser) =", isinstance(tom, AdminUser))

if __name__ == "__main__":
    print("\n--- 07 dunder / isinstance 运行完毕 ---")

# 本文件重点：
# 1. __xxx__ 是协议方法；__str__ 控制 print 长什么样。
# 2. isinstance(obj, Cls) 在继承下更常用。
# 3. type(admin) is User 为 False，但 isinstance(admin, User) 为 True。
# 4. 不要一次记太多魔术方法。
