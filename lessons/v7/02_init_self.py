"""V7-02 __init__ 与 self。

学习目标：
1. 用 __init__ 给实例挂上 name / age。
2. 理解 self 就是当前实例，类似 JS 的 this。
3. 知道定义方法必须写 self，调用时不用手动传。

运行：uv run python lessons/v7/02_init_self.py
"""


class User:
    # ---------------------------------------------------------------------------
    # __init__：实例初始化方法。
    # 用途：User("Tom", 31) 时被调用，给这个新对象填初始数据。
    # JS/TS 对比：≈ constructor(name, age)
    # 注意：严格来说真正「创建空对象」的是 __new__，__init__ 负责初始化。
    #       V7 按 constructor 理解即可，不必展开 __new__。
    # ---------------------------------------------------------------------------
    def __init__(self, name: str, age: int) -> None:
        # self：当前这个实例。
        # JS/TS 对比：≈ this
        # 坑 1：定义时必须显式写在第一个参数。漏写 self，调用 user.xxx() 会对不上参数。
        # 坑 2：调用时不要手动传 self。user.say_hello() 会自动把 user 传进来。
        print("  __init__ 里的 self is 即将赋给变量的那个对象", id(self))
        self.name = name
        self.age = age

    def say_hello(self) -> str:
        return f"Hello, I am {self.name}"


print("创建 tom")
tom = User("Tom", 31)
print("外面的 tom id =", id(tom))
print("tom.name / tom.age =", tom.name, tom.age)
print("tom.say_hello() =", tom.say_hello())
# 等价于显式传入实例，但日常不要这么写：
print("User.say_hello(tom) =", User.say_hello(tom))

print("\n创建 jack")
jack = User("Jack", 17)
print("jack.name =", jack.name)
print("改 tom.name 不会影响 jack")
tom.name = "Thomas"
print("tom.name =", tom.name, "jack.name =", jack.name)

if __name__ == "__main__":
    print("\n--- 02 __init__ / self 运行完毕 ---")

# 本文件重点：
# 1. __init__ ≈ JS constructor，负责给实例填数据。
# 2. self ≈ this，但必须写在方法第一个参数。
# 3. tom.say_hello() 不用传 tom，Python 会自动把实例塞给 self。
# 4. 用 id(self) 和 id(tom) 对照，能直接看出 self 就是这个实例。
