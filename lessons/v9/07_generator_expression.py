"""V9-07 列表推导式 vs Generator Expression。

学习目标：
1. 分清 [] 立刻得到 list，() 得到 generator 并惰性计算。
2. 用 type / next / list 对照两者。
3. 知道大数据时 generator 能减少一次性占内存，但不是永远更快。

运行：uv run python lessons/v9/07_generator_expression.py
"""

nums = [1, 2, 3, 4, 5]

# 列表推导式：立刻算出全部结果，得到完整 list。
doubled_list = [x * 2 for x in nums]
print("列表推导式 type =", type(doubled_list), "值 =", doubled_list)

# Generator Expression：把 [] 换成 ()。
# 返回 generator，按需计算；不会立刻得到完整序列。
# JS/TS 对比：没有完全对应的日常语法；更接近「惰性 map 迭代器」。
doubled_gen = (x * 2 for x in nums)
print("生成器表达式 type =", type(doubled_gen), "对象 =", doubled_gen)
print("第一次 next =", next(doubled_gen))
print("list() 把剩下的一次性收齐 =", list(doubled_gen))

# 内存对比用小数据即可，不要真造几千万条把机器卡住。
# list 版本：函数返回前就已经有 20 个元素的完整容器。
# generator 版本：调用时几乎还没算，for 要一个才产一个。
def eager_squares(n: int) -> list[int]:
    return [i * i for i in range(n)]


def lazy_squares(n: int):
    return (i * i for i in range(n))


eager = eager_squares(20)
lazy = lazy_squares(20)
print("eager 已是完整 list，len =", len(eager))
print("lazy 还是 generator，需要时才算，例如 next =", next(lazy))

# 注意：Generator 的价值主要是惰性处理和减少一次性内存压力，
# 不代表所有场景都更快。小数据用 list 往往更直观。

if __name__ == "__main__":
    print("\n--- 07 Generator Expression 运行完毕 ---")

# 本文件重点：
# 1. [x for x in xs] 立刻得到 list；(x for x in xs) 得到 generator。
# 2. 惰性 = 需要一个才算一个。
# 3. 大数据/流式适合 generator；小数据用 list 更简单。
# 4. generator 不是永远更快，别为了炫技到处改。
