"""V10-07 泛型函数：输入和输出保持同一类型关系。

学习目标：
1. 看懂生态里最常见的 TypeVar("T")。
2. 理解 first / identity 为什么不能简单写成 Any。
3. 眼熟 Python 3.12 的 def first[T](...) 新语法。

运行：uv run python lessons/v10/07_generic_function.py
"""

from typing import TypeVar

# ---------------------------------------------------------------------------
# TypeVar：声明一个类型参数，像 TS 的 T。
# 用途：让「进去什么类型，出来还是什么类型」这件事能被类型系统追踪。
# 不要用 Any：Any 等于放弃检查，输入 list[int] 也可能被当成随便什么。
# 本课不深入 bound / 协变 / 逆变。
# ---------------------------------------------------------------------------
T = TypeVar("T")


def identity(value: T) -> T:
    """进去 T，出来还是 T。"""
    return value


def first(items: list[T]) -> T:
    """list[T] 的第一项仍是 T，而不是 object/Any。"""
    return items[0]


print("identity(1) =", identity(1))
print("identity('Ada') =", identity("Ada"))
print("first([10, 20]) =", first([10, 20]))
print("first(['a', 'b']) =", first(["a", "b"]))


# Python 3.12 新语法：类型参数写在函数名后面。含义与 TypeVar 相同。
def last[T](items: list[T]) -> T:
    return items[-1]


print("last 新语法 =", last([True, False]))

if __name__ == "__main__":
    print("\n--- 07 泛型函数 运行完毕 ---")

# 本文件重点：
# 1. TypeVar 保持输入输出之间的类型关系。
# 2. 主示例用 TypeVar，因为开源库里仍然非常常见。
# 3. Python 3.12 的 def f[T] 更短，先眼熟。
# 4. 用 Any/object 会丢掉「还是原来那个 T」这条信息。
