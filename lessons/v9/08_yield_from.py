"""V9-08 yield from：把另一个 Iterable 的值转发出去。

学习目标：
1. 先写 for + yield，再改成 yield from，看清两者等价。
2. 知道 yield from 只是「继续向外产出别人的元素」。
3. 本课不学 send / throw / 委托底层。

运行：uv run python lessons/v9/08_yield_from.py
"""


def yield_loop(items: list[int]):
    for item in items:
        yield item


def yield_from_items(items: list[int]):
    # yield from iterable：把另一个 Iterable/Generator 的元素逐个向外产出。
    # 用途：拼接多段流、少写一层 for。
    # 等价于：for item in items: yield item
    # 本课只学这个基础用途。
    yield from items


def combined():
    yield "head"
    yield from ["a", "b"]
    yield "tail"


print("普通 for+yield =", list(yield_loop([1, 2, 3])))
print("yield from     =", list(yield_from_items([1, 2, 3])))
print("组合流 =", list(combined()))

if __name__ == "__main__":
    print("\n--- 08 yield from 运行完毕 ---")

# 本文件重点：
# 1. yield from xs  ≈  for x in xs: yield x
# 2. 适合把已有 Iterable/Generator 接到自己的产出流上。
# 3. 先会看、能改写即可，不必抠底层委托。
# 4. send/throw 以及 async generator 本版本不学。
