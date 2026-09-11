"""V9-01 Iterable：能被 for 遍历的东西。

学习目标：
1. 知道 list / tuple / dict / set / str 都是 Iterable。
2. 建立直觉：Iterable = 可以提供迭代器、可以被遍历的对象。
3. 先不深入 collections.abc，只看常见容器。

运行：uv run python lessons/v9/01_iterable.py
"""

# ---------------------------------------------------------------------------
# Iterable（可迭代对象）：可以被 for 遍历的东西。
# 用途：作为「数据来源」交给 for / 推导式 / list() 等去消费。
# 常见坑：能 for 不等于自己就是 Iterator。list 是 Iterable，通常不是 Iterator。
# JS/TS 对比：能 for...of 的对象（实现了 iterable protocol）。
# ---------------------------------------------------------------------------

print("list:")
for item in [1, 2, 3]:
    print(" ", item)

print("tuple:")
for item in ("a", "b"):
    print(" ", item)

print("dict（默认遍历 key）:")
for key in {"name": "Tom", "age": 31}:
    print(" ", key)

print("set:")
for item in {10, 20}:
    print(" ", item)

print("str（按字符）:")
for ch in "hi":
    print(" ", repr(ch))

# for 底层简化理解（不是解释器全部细节）：
# 1. 先 iter(容器) 得到 Iterator
# 2. 不断 next(iterator) 拿下一个值
# 3. 遇到 StopIteration 就结束循环

if __name__ == "__main__":
    print("\n--- 01 Iterable 运行完毕 ---")

# 本文件重点：
# 1. Iterable = 可以被 for 遍历的数据来源。
# 2. list/tuple/dict/set/str 都是常见 Iterable。
# 3. for 能跑，是因为 Python 会帮你取 Iterator，不是 list 自己「神奇循环」。
# 4. Iterable 和 Iterator 不是一回事，下一课分开。
