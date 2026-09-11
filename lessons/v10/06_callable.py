"""V10-06 Callable：把「函数当参数」的签名写清楚。

学习目标：
1. 会读 Callable[[int, int], int]。
2. 结合 filter / calculate 看高阶函数。
3. 能对应到 TS 的 (a: number, b: number) => number。

运行：uv run python lessons/v10/06_callable.py
"""

from typing import Callable

users: list[dict[str, str | int | bool]] = [
    {"name": "Tom", "active": True},
    {"name": "Jack", "active": False},
    {"name": "Ada", "active": True},
]


def is_active(user: dict[str, str | int | bool]) -> bool:
    return bool(user["active"])


def filter_users(
    items: list[dict[str, str | int | bool]],
    predicate: Callable[[dict[str, str | int | bool]], bool],
) -> list[dict[str, str | int | bool]]:
    """predicate 是「收一个 user、返回 bool」的函数。"""
    return [item for item in items if predicate(item)]


# ---------------------------------------------------------------------------
# Callable[[int, int], int]
# 是什么：描述「可调用对象」的参数和返回值。
# 前面的 list：按顺序的参数类型；最后一个类型：返回值。
# 这里：两个 int 参数，返回 int。
# TS 对比：(a: number, b: number) => number
# 运行时：默认不检查你传入的函数到底是不是这个形状。
# ---------------------------------------------------------------------------
def calculate(a: int, b: int, operation: Callable[[int, int], int]) -> int:
    return operation(a, b)


def add(a: int, b: int) -> int:
    return a + b


print("filter active =", filter_users(users, is_active))
print("calculate add =", calculate(2, 3, add))
print("calculate lambda =", calculate(2, 3, lambda x, y: x * y))

if __name__ == "__main__":
    print("\n--- 06 Callable 运行完毕 ---")

# 本文件重点：
# 1. Callable[[参数...], 返回值] 用来标注函数参数。
# 2. 这就是 V3「函数也是对象」在类型上的写法。
# 3. 和 TS 箭头函数类型几乎一一对应。
# 4. 标注不会在运行时强制检查回调签名。
