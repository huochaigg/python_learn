"""用户模型。"""

from dataclasses import dataclass
from typing import Literal

# type 别名（Python 3.12）：给重复出现的基础类型起名字，方便阅读。
# 运行时仍然是 int，不会变成新 class，也不会做校验。
# TS 对比：type UserId = number
type UserId = int

# Literal：把取值限制在几个字面量里（类型检查器用，运行时默认不拦）。
# TS 对比：type Role = "admin" | "user"
type Role = Literal["admin", "user"]


@dataclass
class User:
    """用户。dataclass 仍是真正的 class，不是 TS interface。"""

    id: UserId
    name: str
    role: Role
    active: bool = True
