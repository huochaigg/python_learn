"""V9-03 iter() 和 next()：for 循环帮你做的那两步。

学习目标：
1. 会用 iter(iterable) 拿到 Iterator。
2. 会用 next(iterator) 取值并推进位置。
3. 知道耗尽后抛 StopIteration，以及 next(..., default) 写法。

运行：uv run python lessons/v9/03_iter_next.py
"""

nums = [10, 20, 30]

# iter(iterable)：输入 Iterable，返回 Iterator。
# 用途：手动拿到游标。for 循环第一步就是它。
# 返回值：iterator 对象。会基于源数据创建一个新的遍历状态。
# 是否改源数据：通常不改 list 本身。
iterator = iter(nums)
print("iter(nums) ->", iterator)

# next(iterator)：获取下一个值，并把游标往前推一格。
# 用途：手动一步步消费。for 循环反复做的就是它。
# 返回值：下一项。没有了就抛 StopIteration。
print("next 1 =", next(iterator))
print("next 2 =", next(iterator))
print("next 3 =", next(iterator))

try:
    next(iterator)
except StopIteration:
    # StopIteration：Iterator 协议规定的「没有下一项了」。
    # for 会接住它并安静结束，你手动 next 时就会看到。
    print("第四次 next 抛出 StopIteration")

# next(iterator, default)：耗尽时返回默认值，不抛异常。
done = iter([1])
print("next 有值 =", next(done, None))
print("next 耗尽给默认值 =", next(done, None))

if __name__ == "__main__":
    print("\n--- 03 iter / next 运行完毕 ---")

# 本文件重点：
# 1. iter(x) 从 Iterable 得到 Iterator。
# 2. next(it) 取值并推进状态。
# 3. 耗尽抛 StopIteration；next(it, default) 可以改成返回默认值。
# 4. for 大致 = iter + 反复 next + 吞掉 StopIteration。
