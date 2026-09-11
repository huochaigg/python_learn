"""V11-01 复习：函数是一等对象（为 decorator 铺垫）。

学习目标：
1. 快速回顾：函数能赋值、当参数、当返回值。
2. 知道 decorator 能成立，就是因为函数可以被传递和返回。
3. 不重复展开 V3/V7 的 OOP，只留 decorator 需要的那一层。

运行：uv run python lessons/v11/01_function_as_object_review.py
"""


def greet(name: str) -> str:
    return f"Hello, {name}"


# 函数可以赋值给变量。名字只是标签。
say = greet
print("赋值后调用 =", say("Ada"))


def run(fn, name: str) -> str:
    """函数作为参数：接收一个函数，再调用它。"""
    return fn(name)


print("作为参数 =", run(greet, "Tom"))


def make_greeter(prefix: str):
    """函数作为返回值：返回的是函数本身，还没调用。"""

    def inner(name: str) -> str:
        return f"{prefix}, {name}"

    return inner


hi = make_greeter("Hi")
print("作为返回值再调用 =", hi("Lucy"))

# Decorator 的基础：接收一个函数，返回另一个（通常是包装后的）函数。
# JS/TS 对比：高阶函数。NestJS 的 @Get 也是「包一层横切逻辑」，机制不同。

if __name__ == "__main__":
    print("\n--- 01 函数是对象 运行完毕 ---")

# 本文件重点：
# 1. 函数能当值来传递和返回。
# 2. Decorator 就是建立在这套能力上。
# 3. return inner 是返回函数，return inner() 才是立刻执行。
# 4. 细节下一课从闭包开始。
