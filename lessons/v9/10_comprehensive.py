"""V9-10 综合练习：按需产生订单 ID，而不是先创建全部结果。

学习目标：
1. 综合 Iterable、iter/next、自定义 Iterator、Generator、yield、生成器表达式。
2. 先 TODO，再看示例答案。
3. 场景：订单 ID 分页/批量产生 1～N，按需拿，不先建完整大 list。

运行：uv run python lessons/v9/10_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""


# =============================================================================
# 练习 1
# TODO: 对 ids = ["o-1", "o-2", "o-3"] 使用 iter + next 取出前两个，
#       再用 next(it, None) 安全取出后面的。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")
ids = ["o-1", "o-2", "o-3"]
it = iter(ids)
print(next(it), next(it))
print(next(it, None))
print(next(it, None))


# =============================================================================
# 练习 2
# TODO: 写 OrderIdIterator(max_id)，__iter__/__next__ 产出 "o-1" ... "o-{max_id}"。
#       用 for 打印前 3 个（max_id=3）。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


class OrderIdIterator:
    def __init__(self, max_id: int) -> None:
        self.max_id = max_id
        self.current = 0

    def __iter__(self) -> "OrderIdIterator":
        return self

    def __next__(self) -> str:
        if self.current >= self.max_id:
            raise StopIteration
        self.current += 1
        return f"o-{self.current}"


print(list(OrderIdIterator(3)))


# =============================================================================
# 练习 3
# TODO: 写 generator 函数 order_ids(max_id)，yield "o-1" ...。
#       先 next 两次，再 list() 收剩余。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


def order_ids(max_id: int):
    current = 1
    while current <= max_id:
        yield f"o-{current}"
        current += 1


gen = order_ids(5)
print("next =", next(gen), next(gen))
print("剩余 =", list(gen))
print("同一对象再 list =", list(gen), "（已空，需重新调用 order_ids）")


# =============================================================================
# 练习 4
# TODO: 用生成器表达式产出 1～10 中偶数订单 ID，再 list() 查看。
#       对比等价列表推导式。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")
eager = [f"o-{n}" for n in range(1, 11) if n % 2 == 0]
lazy = (f"o-{n}" for n in range(1, 11) if n % 2 == 0)
print("list 推导式 =", eager)
print("生成器表达式 type =", type(lazy), "值 =", list(lazy))


# =============================================================================
# 练习 5
# TODO: 写 batch_order_ids()：先 yield from order_ids(3)，再 yield "o-extra"。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")


def batch_order_ids():
    yield from order_ids(3)
    yield "o-extra"


print("batch =", list(batch_order_ids()))

if __name__ == "__main__":
    print("\n--- 10 综合练习 运行完毕 ---")

# 本文件重点：
# 1. iter/next 是 for 的手工版。
# 2. 自定义 Iterator 和 Generator 都能按需产出订单 ID。
# 3. yield 暂停；generator object 用完要重新调用函数。
# 4. () 是惰性的；yield from 用来拼接流。
