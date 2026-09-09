"""V3-05 lambda：只能写一个表达式的匿名函数。

学习目标：
1. 能把 lambda x: x * 2 对应到 JS 的 x => x * 2。
2. 会用 sorted(..., key=...) 按对象的某个字段排序。
3. 知道 map / filter 返回的是惰性对象，需要时再 list(...) 。
4. 复杂逻辑不要硬写 lambda，改用普通 def。

运行：uv run python lessons/v3/05_lambda.py
"""

# ---------------------------------------------------------------------------
# lambda：匿名函数，只能写一个表达式，不能写语句（没有块级函数体）。
# JS/TS 对比：lambda x: x * 2  ≈  x => x * 2
# 注意：JS 箭头函数可以写 { return ... } 多行；Python lambda 不行。
# ---------------------------------------------------------------------------
double = lambda x: x * 2
print("double(5) =", double(5))


users: list[dict[str, str | int]] = [
    {"name": "Tom", "age": 31},
    {"name": "Jack", "age": 17},
    {"name": "Lucy", "age": 25},
]

# ---------------------------------------------------------------------------
# sorted 的 key 参数：告诉 sorted「拿每个元素的什么值当排序依据」。
# 参数：
#   iterable: 要排序的序列
#   key: 一个函数，接收单个元素，返回用来比较的值
#   reverse: 是否倒序，默认 False
# 返回：新 list，不修改原对象。
# JS/TS 对比：users.toSorted((a, b) => a.age - b.age)
# Python 更常见：sorted(users, key=lambda u: u["age"])
# ---------------------------------------------------------------------------
by_age = sorted(users, key=lambda user: user["age"])
print("按 age 排序 =", by_age)
print("原 users 未被修改 =", users)

by_name = sorted(users, key=lambda user: user["name"])
print("按 name 排序 =", by_name)


# ---------------------------------------------------------------------------
# map：对每个元素应用函数。返回惰性 map 对象，不是 list。
# filter：留下让函数为真的元素。同样是惰性的。
# JS/TS 对比：≈ array.map / array.filter，但 Python 这两货不会立刻算出数组。
# 注意：实际项目里列表推导式往往更直观，这两个 API 先混眼熟即可。
# ---------------------------------------------------------------------------
nums = [1, 2, 3, 4]
mapped = map(lambda x: x * 2, nums)
print("map 对象本身 =", mapped)
print("list(map(...)) =", list(mapped))
print("list(filter(...)) =", list(filter(lambda x: x % 2 == 0, nums)))

# 同一件事用推导式通常更好读：
print("推导式翻倍 =", [x * 2 for x in nums])
print("推导式偶数 =", [x for x in nums if x % 2 == 0])


# 复杂逻辑用普通 def，不要把 lambda 写成谜语。
def age_of(user: dict[str, str | int]) -> int:
    """给 sorted 用的 key 函数，逻辑一多就该写成 def。"""
    return int(user["age"])


print("用 def 作为 key =", sorted(users, key=age_of))

if __name__ == "__main__":
    print("\n--- 05 lambda 运行完毕 ---")

# 本文件重点：
# 1. lambda 只能写一个表达式，对应 JS 最简单的箭头函数。
# 2. sorted(items, key=lambda x: x["age"]) 是后端里最常见的 lambda 用法。
# 3. map / filter 返回惰性对象，要看内容先 list(...)；多数情况推导式更清晰。
# 4. 逻辑稍复杂就写 def，不要为了匿名而匿名。
