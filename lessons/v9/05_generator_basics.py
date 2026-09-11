"""V9-05 Generator 基础：带 yield 的函数会返回生成器对象。

学习目标：
1. 对比「普通函数 return list」和「yield 生成器」。
2. 知道调用生成器函数不会立刻跑完函数体。
3. 记住：yield 产出并暂停；return 产出并结束。

运行：uv run python lessons/v9/05_generator_basics.py
"""


def build_list() -> list[int]:
    """普通函数：一上来就把全部结果算完，装进 list 返回。"""
    print("  build_list 开始，立刻算完全部")
    result = []
    for n in [1, 2, 3]:
        result.append(n)
    print("  build_list 结束，一次返回整箱数据")
    return result


def count_up():
    # yield：产出一个值并暂停函数，保存局部状态。
    # 和 return 的区别：return 通常结束函数；yield 是「返回并暂停」。
    # 带 yield 的函数叫 Generator Function；调用它得到 Generator Object（也是 Iterator）。
    # JS/TS 对比：function* 里的 yield，思想接近，语法不同。
    print("  generator 函数体：还没到第一个 yield")
    yield 1
    yield 2
    yield 3


print("调用普通函数，立刻拿到 list:")
nums = build_list()
print("  结果 =", nums, "type =", type(nums))

print("\n调用生成器函数，只拿到 Generator Object:")
gen = count_up()
print("  type(gen) =", type(gen))
print("  注意：上面几乎没有打印「函数体」日志，说明还没真正执行")

print("第一次 next 才开始跑到第一个 yield:")
print("  ", next(gen))
print("再 next:")
print("  ", next(gen))
print("  ", next(gen))

if __name__ == "__main__":
    print("\n--- 05 Generator 基础 运行完毕 ---")

# 本文件重点：
# 1. Generator Function 调用返回 Generator Object，不是最终结果。
# 2. Generator 本质上是 Iterator，可以 next / for。
# 3. yield = 产出并暂停；return = 结束。
# 4. 这是 Python 帮你实现 Iterator 协议的快捷方式。
