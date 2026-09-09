"""V3-07 函数也是对象：赋值、当参数、当返回值。

学习目标：
1. 把函数赋值给变量后，仍然可以调用。
2. 会写把函数当参数传入的简单高阶函数。
3. 会返回一个函数，而不是立刻执行它。
4. 先记住：装饰器就是建立在这个能力上，本版本不学 decorator。

运行：uv run python lessons/v3/07_function_as_object.py
"""


def add(a: int, b: int) -> int:
    """两数相加。"""
    return a + b


def mul(a: int, b: int) -> int:
    """两数相乘。"""
    return a * b


# ---------------------------------------------------------------------------
# 函数可以赋值给变量。名字只是标签，真正能调用的是函数对象。
# JS/TS 对比：const op = add; op(2, 3)
# ---------------------------------------------------------------------------
op = add
print("op is add =", op is add)
print("op(2, 3) =", op(2, 3))


# ---------------------------------------------------------------------------
# 函数可以作为参数传递。
# run_operation 自己不知道怎么算，只负责调用传入的 fn。
# JS/TS 对比：function runOperation(fn, a, b) { return fn(a, b) }
# ---------------------------------------------------------------------------
def run_operation(fn, a: int, b: int) -> int:
    """接收一个二元函数并执行。fn 是参数，不是字符串。"""
    return fn(a, b)


print("run_operation(add, 2, 3) =", run_operation(add, 2, 3))
print("run_operation(mul, 2, 3) =", run_operation(mul, 2, 3))
print("run_operation(lambda x, y: x - y, 2, 3) =", run_operation(lambda x, y: x - y, 2, 3))


# ---------------------------------------------------------------------------
# 函数可以作为返回值：返回的是函数本身，还没调用。
# 注意：pick_operation("add") 得到 add；pick_operation("add")(2, 3) 才会算出 5。
# JS/TS 对比：return add 和 return add() 的区别，两边一样重要。
# ---------------------------------------------------------------------------
def pick_operation(name: str):
    """按名字返回对应函数。"""
    if name == "mul":
        return mul
    return add


picked = pick_operation("mul")
print("返回的函数对象 =", picked)
print("再调用 picked(4, 5) =", picked(4, 5))

# 装饰器后续就是建立在「函数可以作为对象传递」这个基础上。
# 本版本先看到这里，不要提前学 @decorator 语法。

if __name__ == "__main__":
    print("\n--- 07 函数作为对象 运行完毕 ---")

# 本文件重点：
# 1. 函数能赋值、能当参数、能当返回值，和 JS 一阶函数一样。
# 2. run_operation(fn, a, b) 是最典型的高阶函数形态。
# 3. return add 是返回函数；return add() 是返回调用结果。
# 4. 装饰器以后再学，现在只需接受「函数也是值」。
