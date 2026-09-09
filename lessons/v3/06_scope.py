"""V3-06 作用域：局部变量、全局变量、global。

学习目标：
1. 理解函数内部赋值默认创建局部变量。
2. 知道 global 可以改外层全局变量。
3. 明确：正式后端项目不要大量依赖全局可变状态。

运行：uv run python lessons/v3/06_scope.py
"""

# 函数外定义的是全局变量。
counter = 0
name = "global-name"


def read_global() -> str:
    """函数内部只读取全局变量，不赋值，用的就是外面的 name。"""
    return name


print("读取全局 name =", read_global())


def assign_local() -> str:
    """函数内部一旦赋值，这个名字就是局部变量。

    注意：这里的 name 和外面的全局 name 不是同一个。
    JS/TS 对比：function 里 const name = ... 也不会改到外层同名变量。
    """
    name = "local-name"
    return name


print("函数内赋值得到局部变量 =", assign_local())
print("全局 name 没被改掉 =", name)


def bump_without_global() -> None:
    """只赋值、不写 global 时，counter 是局部变量。

    注意：如果这里写 counter = counter + 1，会 UnboundLocalError，
    因为赋值让 Python 把 counter 当成局部变量，而局部又还没定义。
    """
    counter = 100
    print("  函数内的局部 counter =", counter)


bump_without_global()
print("没使用 global，外面的 counter 仍是", counter)


# ---------------------------------------------------------------------------
# global：声明「我要改的是模块顶层那个变量」。
# 注意：这只是让你看懂语法。正式后端项目不要大量使用全局可变状态，
# 数据应通过函数参数传入、通过返回值传出，或放到明确的对象/依赖里。
# 后续 FastAPI 中会经常出现：用 Depends 注入，而不是改全局变量。
# ---------------------------------------------------------------------------
def bump_with_global() -> None:
    """演示 global。知道即可，项目里尽量别用。"""
    global counter
    counter += 1


bump_with_global()
bump_with_global()
print("用了 global 之后 counter =", counter)

if __name__ == "__main__":
    print("\n--- 06 作用域 运行完毕 ---")

# 本文件重点：
# 1. 函数内赋值 → 局部变量；只读取、不赋值 → 可以用到全局变量。
# 2. 要修改全局变量必须写 global，但正式项目应避免这样做。
# 3. 闭包和 nonlocal 本版本不展开，后续再学。
# 4. 后端更推荐：参数进、返回值出，而不是藏在全局状态里。
