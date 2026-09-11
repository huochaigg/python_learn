"""V10-11 综合练习：订单查询场景把本版类型串起来。

学习目标：
1. 综合 list[T]、| None、Literal、type 别名、TypedDict、Callable、Generic。
2. 先 TODO，再对照示例答案。
3. 场景：订单状态过滤 + 分页结果。

运行：uv run python lessons/v10/11_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

from typing import Callable, Generic, Literal, TypeVar, TypedDict

T = TypeVar("T")

# =============================================================================
# 练习 1
# TODO: 定义 type OrderId = int，以及 OrderStatus = Literal["pending", "paid"]。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")
type OrderId = int
OrderStatus = Literal["pending", "paid"]
print("OrderId example =", 101)
print("statuses = pending | paid")


# =============================================================================
# 练习 2
# TODO: 写 TypedDict Order，字段 id: OrderId, amount: int, status: OrderStatus。
#       建一个 pending 订单并打印。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


class Order(TypedDict):
    id: OrderId
    amount: int
    status: OrderStatus


orders: list[Order] = [
    {"id": 1, "amount": 50, "status": "pending"},
    {"id": 2, "amount": 80, "status": "paid"},
    {"id": 3, "amount": 20, "status": "pending"},
]
print("orders =", orders)


# =============================================================================
# 练习 3
# TODO: 写 filter_orders(items, predicate: Callable[[Order], bool]) -> list[Order]。
#       用 lambda 或函数筛出 paid。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


def filter_orders(items: list[Order], predicate: Callable[[Order], bool]) -> list[Order]:
    return [item for item in items if predicate(item)]


paid = filter_orders(orders, lambda order: order["status"] == "paid")
print("paid =", paid)


# =============================================================================
# 练习 4
# TODO: 写 Generic 类 PageResult[T]，字段 items: list[T], total: int。
#       用 PageResult[Order] 包住 pending 订单。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


class PageResult(Generic[T]):
    def __init__(self, items: list[T], total: int) -> None:
        self.items = items
        self.total = total

    def __repr__(self) -> str:
        return f"PageResult(total={self.total}, items={self.items!r})"


def list_orders(status: OrderStatus | None = None) -> PageResult[Order]:
    items = orders
    if status is not None:
        items = [order for order in items if order["status"] == status]
    return PageResult(items, total=len(items))


print("pending page =", list_orders("pending"))
print("all page =", list_orders())

if __name__ == "__main__":
    print("\n--- 11 综合练习 运行完毕 ---")

# 本文件重点：
# 1. OrderId / Literal 把 id 和 status 说清楚。
# 2. TypedDict 描述订单 dict。
# 3. Callable 是过滤器签名；PageResult[T] 是分页壳。
# 4. status: OrderStatus | None = None 才表示「可以不传；传了也可以是 None」。
