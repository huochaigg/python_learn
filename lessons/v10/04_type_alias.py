"""V10-04 类型别名：给复杂或重复出现的类型起名字。

学习目标：
1. 用 Python 3.12 的 type Xxx = ... 写别名。
2. 能看懂旧项目里的 TypeAlias。
3. 不要把别名写得太嵌套。

运行：uv run python lessons/v10/04_type_alias.py
"""

from typing import TypeAlias

# ---------------------------------------------------------------------------
# type 别名（Python 3.12）：给类型起一个可读的名字。
# 用途：UserId、UserMap 这种在多处重复的结构。
# 运行时：主要还是静态含义；不要指望它变成新的 class。
# TS 对比：type UserId = number
# ---------------------------------------------------------------------------
type UserId = int
type UserMap = dict[str, str]


def get_name(users: UserMap, user_id: UserId) -> str | None:
    return users.get(str(user_id))


users: UserMap = {"1": "Tom", "2": "Ada"}
print("get_name =", get_name(users, 1))

# 旧项目阅读用：TypeAlias 明确告诉工具「这是别名，不是普通变量」。
# 本课只在这里示范一次，后面统一用 type Xxx = ...
LegacyUserId: TypeAlias = int
legacy_id: LegacyUserId = 99
print("legacy id =", legacy_id)

if __name__ == "__main__":
    print("\n--- 04 类型别名 运行完毕 ---")

# 本文件重点：
# 1. 当前项目基准是 Python 3.12，优先 type UserId = int。
# 2. TypeAlias 是为了读历史代码，不要两种写法混着用。
# 3. 别名让签名更短，不会凭空多出运行时校验。
# 4. 别设计过深的嵌套类型，读起来会比不写别名更差。
