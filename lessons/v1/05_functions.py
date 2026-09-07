"""V1-05 函数：定义、参数、返回值、默认参数。

运行：uv run python lessons/v1_basics/05_functions.py
"""


def greet(name: str) -> str:
    """返回一句问候。文档字符串写函数干什么。"""
    return f"Hello, {name}!"


def add(a, b=10):
    """b 有默认值：不传 b 时用 10。"""
    return a + b


def stats(*nums):
    """*nums 把多余的位置参数收成元组。"""
    return sum(nums), len(nums)


def show_info(**kwargs):
    """**kwargs 把多余的关键字参数收成字典。"""
    return kwargs


print(greet("Ada"))
print("add(3) =", add(3))
print("add(3, 4) =", add(3, 4))
print("stats(1, 2, 3, 4) =", stats(1, 2, 3, 4))
print("show_info(name='Ada', age=28) =", show_info(name="Ada", age=28))

# lambda：只能写一个表达式的匿名小函数
square = lambda x: x * x
print("square(5) =", square(5))


# 没有 return，或 return 后面不写值，结果都是 None
def do_nothing():
    print("  我执行了，但没有返回有用的值")


print("do_nothing() 的返回值 =", do_nothing())

if __name__ == "__main__":
    print("\n--- 05 函数 运行完毕 ---")
