"""V10-03 Literal：只允许几个固定字面量。

学习目标：
1. 会用 Literal 描述角色、订单状态、排序方向。
2. 能对应到 TS 的 "admin" | "user"。
3. 知道普通 Python 不会因为传了错字符串就自动运行时失败。

运行：uv run python lessons/v10/03_literal.py
"""

from typing import Literal

# ---------------------------------------------------------------------------
# Literal：把类型收窄成几个具体字面量。
# 用途：role / status / sort 这种封闭枚举字符串。
# 类型参数：列出允许的值。
# 运行时：默认不校验。传 "super-admin" 解释器通常照样跑。
# TS 对比：type Role = "admin" | "user"
# ---------------------------------------------------------------------------
Role = Literal["admin", "user"]
OrderStatus = Literal["pending", "paid", "cancelled"]
SortDir = Literal["asc", "desc"]


def set_role(role: Role) -> str:
    return f"role={role}"


def list_orders(status: OrderStatus, sort: SortDir = "asc") -> str:
    return f"status={status} sort={sort}"


print(set_role("admin"))
print(list_orders("paid", "desc"))

# 静态检查会认为 "guest" 不合法；运行时下一行仍然能执行。
print("运行时错误字符串也能过 =", set_role("guest"))  # type: ignore[arg-type]

if __name__ == "__main__":
    print("\n--- 03 Literal 运行完毕 ---")

# 本文件重点：
# 1. Literal["admin", "user"] ≈ TS "admin" | "user"。
# 2. 适合后端里封闭的状态机字符串。
# 3. 普通 Python 不会自动做运行时枚举校验。
# 4. 以后 Pydantic 可以用类似标注在请求体里真正拦住非法值。
