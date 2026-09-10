"""V8-05 property setter：赋值看起来像改字段，实际走校验。

学习目标：
1. 对外仍写 user.age / user.age = 31，对内存 self._age。
2. 理解 setter 里不能再写 self.age = value，否则递归。
3. 非法值 raise ValueError，和 V5 异常处理接上。

运行：uv run python lessons/v8/05_property_setter.py
"""


class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        # 初始化也走 setter，这样构造时就能校验。
        self.age = age

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        # @age.setter：给同名 property 配 setter。
        # 用途：user.age = 31 时做校验或转换。
        # JS/TS 对比：set age(value) { ... }
        # 内部存 _age：单下划线只是「内部约定」，不是严格 private。
        # 坑：这里如果写 self.age = value，会再次进入 setter，无限递归。
        if value < 0:
            raise ValueError("age must be >= 0")
        self._age = value


tom = User("Tom", 31)
print("读取 tom.age =", tom.age)
tom.age = 32
print("赋值后 tom.age =", tom.age)
print("真实存放在 tom._age =", tom._age)

try:
    tom.age = -1
except ValueError as e:
    print("setter 里 raise =", e)

try:
    User("Jack", -8)
except ValueError as e:
    print("构造时同样走 setter =", e)

if __name__ == "__main__":
    print("\n--- 05 property setter 运行完毕 ---")

# 本文件重点：
# 1. 对外 age，对内 _age，避免 setter 自己调自己。
# 2. user.age = 31 会执行函数，不是单纯改字段。
# 3. 非法赋值 raise ValueError，调用方用 try/except。
# 4. _age 能被外面读到，这只是约定，不是 TS private。
