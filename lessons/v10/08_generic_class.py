"""V10-08 泛型类：ApiResponse[T] / Box[T]。

学习目标：
1. 会读 class ApiResponse(Generic[T])。
2. 看懂 ApiResponse[User] 和 ApiResponse[list[User]]。
3. 眼熟 Python 3.12 的 class Box[T]。

运行：uv run python lessons/v10/08_generic_class.py
"""

from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class User:
    name: str
    age: int


# ---------------------------------------------------------------------------
# Generic[T]：这个类的「数据槽」类型由使用方填。
# 用途：统一响应、分页、容器。后面 FastAPI 里常见 { data: T, ok: bool }。
# ApiResponse[User] 的 data 是 User；ApiResponse[list[User]] 的 data 是用户列表。
# 运行时：默认不做 T 的校验，只是给静态工具看。
# TS 对比：class ApiResponse<T> { data: T }
# ---------------------------------------------------------------------------
class ApiResponse(Generic[T]):
    def __init__(self, data: T, ok: bool = True) -> None:
        self.data = data
        self.ok = ok

    def __repr__(self) -> str:
        return f"ApiResponse(ok={self.ok}, data={self.data!r})"


user_res: ApiResponse[User] = ApiResponse(User("Tom", 31))
list_res: ApiResponse[list[User]] = ApiResponse([User("Tom", 31), User("Ada", 30)])
print(user_res)
print(list_res)


class PageResult(Generic[T]):
    def __init__(self, items: list[T], total: int) -> None:
        self.items = items
        self.total = total


page = PageResult[User]([User("Ada", 30)], total=1)
print("page.total =", page.total, "first =", page.items[0])


# Python 3.12 新语法，不必再写 Generic[T]。
class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value


print("Box 新语法 =", Box("ok").value)

if __name__ == "__main__":
    print("\n--- 08 泛型类 运行完毕 ---")

# 本文件重点：
# 1. Generic[T] 让同一个响应壳装不同类型的 data。
# 2. ApiResponse[User] 和 ApiResponse[list[User]] 不是同一种响应。
# 3. 分页 PageResult[T] 也是同一套路。
# 4. 3.12 的 class Box[T] 先会看即可，库代码里 Generic[T] 仍然很多。
