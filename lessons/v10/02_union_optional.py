"""V10-02 Union 与 Optional：| 写法，以及「允许 None ≠ 可以不传」。

学习目标：
1. 优先用 Python 3.12 的 str | int、str | None。
2. 能看懂旧代码里的 Union / Optional。
3. 分清：允许 None，和参数可以省略，是两件事。

运行：uv run python lessons/v10/02_union_optional.py
"""

from typing import Optional, Union

# ---------------------------------------------------------------------------
# Union：值可以是其中某一种类型。现代写法 A | B。
# 用途：接口可能返回 str 或 int、成功或失败值等。
# 运行时：默认不验证，传了第三种类型也不一定立刻炸。
# TS 对比：string | number
# Optional[str]：旧写法，等价于 str | None。
# ---------------------------------------------------------------------------

def parse_id(raw: str | int) -> str:
    return str(raw)


def parse_id_legacy(raw: Union[str, int]) -> str:
    """旧项目常见写法，含义和 str | int 一样。"""
    return str(raw)


print("parse_id(1) =", parse_id(1))
print("parse_id('u1') =", parse_id("u1"))
print("legacy =", parse_id_legacy("u2"))


def describe(name: str | None) -> str:
    # str | None：允许传入 None，不等于调用时可以不传这个参数。
    # TS 对比：
    #   name: string | null     → 允许 null，调用仍要传
    #   name?: string           → 参数可省略
    # Python：只有再加 = None，调用才能省略。
    if name is None:
        return "anonymous"
    return name


print("describe('Tom') =", describe("Tom"))
print("describe(None) =", describe(None))
# describe()  # 注意：这行会 TypeError，缺参数。允许 None ≠ 可以不传。


def describe_optional(name: str | None = None) -> str:
    """加了默认值，调用时才可以不传。"""
    return describe(name)


print("describe_optional() =", describe_optional())

legacy_name: Optional[str] = None
print("Optional[str] 旧写法 =", legacy_name)

if __name__ == "__main__":
    print("\n--- 02 Union / Optional 运行完毕 ---")

# 本文件重点：
# 1. Python 3.10+ 推荐 A | B；Union[A, B] 是历史写法。
# 2. T | None 表示允许 None；Optional[T] 等价于它。
# 3. 允许 None 不等于参数可省略；可省略通常还要 = None。
# 4. 标注本身不做运行时联合类型检查。
