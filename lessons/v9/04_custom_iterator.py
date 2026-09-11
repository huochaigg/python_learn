"""V9-04 手写 Iterator：__iter__ / __next__ / StopIteration。

学习目标：
1. 自己实现一个只会往前走的计数 Iterator。
2. 看懂 for 会自动调用这套协议，并处理 StopIteration。
3. 不深入 C 实现，只把协议跑通。

运行：uv run python lessons/v9/04_custom_iterator.py
"""


class CountIterator:
    """从 1 数到 max_value。自己就是 Iterator。"""

    def __init__(self, max_value: int) -> None:
        self.max_value = max_value
        self.current = 0

    def __iter__(self) -> "CountIterator":
        # __iter__()：让对象能进入 for。
        # 用途：返回 Iterator。Iterator 通常返回 self；
        #       纯 Iterable（如 list）则会返回一个新的 iterator 对象。
        return self

    def __next__(self) -> int:
        # __next__()：返回下一个元素，并推进内部状态。
        # 没有下一项时必须 raise StopIteration，否则 for 不知道何时停。
        if self.current >= self.max_value:
            raise StopIteration
        self.current += 1
        return self.current


counter = CountIterator(3)
print("手动 next:", next(counter), next(counter), next(counter))
try:
    next(counter)
except StopIteration:
    print("手动耗尽，StopIteration")

print("for 会自动 iter + next + 处理 StopIteration:")
for n in CountIterator(3):
    print(" ", n)

if __name__ == "__main__":
    print("\n--- 04 自定义 Iterator 运行完毕 ---")

# 本文件重点：
# 1. Iterator 至少要有 __iter__ 和 __next__。
# 2. __next__ 没数据时 raise StopIteration。
# 3. for obj in xxx 会走这套协议，你不必自己 catch StopIteration。
# 4. 手写 Iterator 是为了理解协议；日常更常用 Generator。
