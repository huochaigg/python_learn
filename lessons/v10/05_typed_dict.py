"""V10-05 TypedDict：给「固定字段的 dict」做类型说明。

学习目标：
1. 会写 UserDict / OrderDict。
2. 对比 dict[str, object] 为什么说不清字段。
3. 不要把 TypedDict 和 dataclass / Pydantic 混为一谈。

运行：uv run python lessons/v10/05_typed_dict.py
"""

from typing import TypedDict

# ---------------------------------------------------------------------------
# TypedDict：描述「键固定、值类型已知」的 dict。
# 用途：JSON 输入、函数间传递的结构化字典。
# 运行时：仍然是普通 dict，默认不会按字段校验。
# TS 对比：很像 interface { name: string; age: number }
# 注意：它不是 class 实例，也不是 dataclass，更不是 Pydantic BaseModel。
# ---------------------------------------------------------------------------


class UserDict(TypedDict):
    id: int
    name: str
    active: bool


class OrderDict(TypedDict):
    id: int
    user_id: int
    amount: int


user: UserDict = {"id": 1, "name": "Tom", "active": True}
order: OrderDict = {"id": 10, "user_id": 1, "amount": 99}
print("user =", user)
print("order =", order)
print("仍然是 dict =", type(user), user["name"])

# dict[str, object]：只知道「字符串键 → 某种对象」，不知道有哪些字段。
loose: dict[str, object] = {"id": 1, "name": "Tom"}
print("loose['name'] =", loose["name"])
# 静态工具很难知道 loose["name"] 一定是 str。

if __name__ == "__main__":
    print("\n--- 05 TypedDict 运行完毕 ---")

# 本文件重点：
# 1. TypedDict 给固定结构的 dict 提供字段级类型。
# 2. 运行时还是 dict，访问用 user["name"]。
# 3. 和 dataclass（真对象）/ Pydantic（校验 DTO）职责不同。
# 4. dict[str, object] 太宽，描述不了后端 JSON 形状。
