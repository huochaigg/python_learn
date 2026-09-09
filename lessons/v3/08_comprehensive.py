"""V3-08 综合练习：默认参数、关键字参数、*args、**kwargs、lambda 排序、函数当参数。

学习目标：
1. 独立完成下面练习，把 V3 核心点串起来。
2. 先在 TODO 区域自己写，再往下看示例答案。
3. 打断点对比你的变量和示例答案。

运行：uv run python lessons/v3/08_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

orders: list[dict[str, int | str]] = [
    {"id": 1, "user": "Tom", "amount": 120, "status": "paid"},
    {"id": 2, "user": "Jack", "amount": 50, "status": "pending"},
    {"id": 3, "user": "Lucy", "amount": 200, "status": "paid"},
    {"id": 4, "user": "Mike", "amount": 80, "status": "cancelled"},
]


# =============================================================================
# 练习 1
# TODO: 写函数 create_order(user, amount, status="pending")，返回一个 dict。
#       用关键字参数调用一次：create_order(user="Ada", amount=99)
# JS/TS 对比：默认参数很像；关键字调用更接近传 options 对象。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


def create_order(user: str, amount: int, status: str = "pending") -> dict[str, int | str]:
    """创建订单。status 有默认值，调用时推荐写关键字。"""
    return {"user": user, "amount": amount, "status": status}


new_order = create_order(user="Ada", amount=99)
print("new_order =", new_order)


# =============================================================================
# 练习 2
# TODO: 写 add_tag(tag, tags=None)，正确处理可变默认参数。
#       连续调用两次、都不传入 tags，确认两次得到的不是同一个 list。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """默认 None，内部再新建 list，避免复用同一个默认对象。"""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags


tags_a = add_tag("vip")
tags_b = add_tag("urgent")
print("tags_a =", tags_a)
print("tags_b =", tags_b)
print("两次不是同一个 list =", tags_a is not tags_b)


# =============================================================================
# 练习 3
# TODO: 写 total(*args)，把任意多个金额加起来。
#       再准备 amounts = [120, 50, 200]，用 total(*amounts) 调用。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


def total(*args: int) -> int:
    """*args 在定义时收集成 tuple。"""
    return sum(args)


amounts = [120, 50, 200]
print("total(1, 2, 3) =", total(1, 2, 3))
print("total(*amounts) =", total(*amounts))


# =============================================================================
# 练习 4
# TODO: 写 describe_order(**kwargs)，把关键字参数收成 dict 并返回。
#       用 describe_order(**orders[0]) 调用。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


def describe_order(**kwargs) -> dict:
    """**kwargs 在定义时收集成 dict；调用时 **orders[0] 是展开。"""
    return kwargs


print("describe_order(user='Tom', amount=120) =", describe_order(user="Tom", amount=120))
print("describe_order(**orders[0]) =", describe_order(**orders[0]))


# =============================================================================
# 练习 5
# TODO: 用 sorted + lambda，按 amount 从小到大排序 orders。
#       不要修改原 orders。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")
sorted_orders = sorted(orders, key=lambda order: order["amount"])
print("sorted_orders =", sorted_orders)
print("原 orders 第一项仍是 Tom =", orders[0]["user"])


# =============================================================================
# 练习 6
# TODO: 写 run_on_orders(fn, items)，对每个订单调用 fn，收集结果。
#       传入一个 lambda 或普通函数，取出所有 user 名字。
# JS/TS 对比：items.map(fn)
# =============================================================================
print("\n===== 练习 6 TODO =====")


print("===== 练习 6 示例答案 =====")


def run_on_orders(fn, items: list[dict[str, int | str]]) -> list:
    """函数作为参数：自己不关心 fn 做什么，只负责逐个调用。"""
    result = []
    for item in items:
        result.append(fn(item))
    return result


user_names = run_on_orders(lambda order: order["user"], orders)
print("user_names =", user_names)


# =============================================================================
# 练习 7
# TODO: 把上面得到的关键结果打印成一份摘要。
# =============================================================================
print("\n===== 练习 7 TODO =====")


print("===== 练习 7 示例答案 =====")
print("---------- 处理结果 ----------")
print("new_order =", new_order)
print("tags_a / tags_b =", tags_a, tags_b)
print("total(*amounts) =", total(*amounts))
print("sorted amounts =", [order["amount"] for order in sorted_orders])
print("user_names =", user_names)

if __name__ == "__main__":
    print("\n--- 08 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 关键字参数让调用更可读：create_order(user="Ada", amount=99)。
# 2. 可变默认参数用 None，不要直接 []。
# 3. 定义时 *args/**kwargs 是收集，调用时 *data/**data 是展开。
# 4. sorted(..., key=lambda ...) 和把函数当参数，是 V3 最实用的两个组合。
