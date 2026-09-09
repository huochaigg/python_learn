"""V2-05 推导式：list / dict / set comprehension。

学习目标：
1. 能把普通 for 循环改写成列表推导式，也能改回来。
2. 掌握带 if 的过滤，以及 map + filter 组合。
3. 会写字典推导式、集合推导式。
4. 知道：简单时用推导式，复杂逻辑不要硬挤成一行。

运行：uv run python lessons/v2/05_comprehensions.py
"""

nums: list[int] = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------------------
# 列表推导式：先看普通版本，再看压缩后的版本。
# JS/TS 对比：≈ nums.map(num => num * 2)
# ---------------------------------------------------------------------------
result: list[int] = []
for num in nums:
    result.append(num * 2)
print("普通 for 翻倍 =", result)

result = [num * 2 for num in nums]
print("列表推导式翻倍 =", result)

# ---------------------------------------------------------------------------
# 带 if：先过滤再收集。
# JS/TS 对比：≈ nums.filter(num => num % 2 === 0)
# ---------------------------------------------------------------------------
evens = [num for num in nums if num % 2 == 0]
print("偶数 =", evens)

# ---------------------------------------------------------------------------
# map + filter 组合：先过滤，再映射。
# JS/TS 对比：≈ nums.filter(n => n % 2 === 0).map(n => n * 10)
# 阅读顺序：先看 for，再看 if，最后看要产出的表达式。
# ---------------------------------------------------------------------------
mapped = [
    num * 10
    for num in nums
    if num % 2 == 0
]
print("偶数 * 10 =", mapped)

# ---------------------------------------------------------------------------
# 字典推导式：产出 dict。
# JS/TS 对比：没有字面量推导；通常 Object.fromEntries(nums.map(n => [n, n * n]))
# ---------------------------------------------------------------------------
squares = {
    num: num * num
    for num in nums
}
print("平方 dict =", squares)

# ---------------------------------------------------------------------------
# 集合推导式：产出 set，顺便去重。
# JS/TS 对比：≈ new Set(nums.map(n => n * 2))
# ---------------------------------------------------------------------------
doubled_set = {
    num * 2
    for num in nums
}
print("加倍后的 set =", doubled_set)

# ---------------------------------------------------------------------------
# 用真实一点的数据：取出 active 用户的 name。
# 要求：普通 for 和推导式各写一遍，对照转换关系。
# JS/TS 对比：
#   users.filter(u => u.active).map(u => u.name)
# ---------------------------------------------------------------------------
users: list[dict[str, int | str | bool]] = [
    {"id": 1, "name": "Tom", "active": True},
    {"id": 2, "name": "Jack", "active": False},
    {"id": 3, "name": "Lucy", "active": True},
]

active_names: list[str] = []
for user in users:
    if user["active"]:
        active_names.append(user["name"])
print("普通 for 得到 active names =", active_names)

active_names = [user["name"] for user in users if user["active"]]
print("推导式得到 active names =", active_names)

# 注意：
# 简单映射/过滤，推导式很合适。
# 循环体一旦有多层 if、副作用、多步计算，就写回普通 for，优先可读性。
# 实际项目不要为了「一行」牺牲清晰度。

if __name__ == "__main__":
    print("\n--- 05 推导式 运行完毕 ---")

# 本文件重点：
# 1. [表达式 for x in xs] ≈ map；再加 if ≈ filter。
# 2. 阅读顺序：for → if → 表达式。
# 3. {k: v for ...} 是 dict；{x for ...} 是 set。
# 4. 复杂逻辑用普通 for，不要强行一行推导式。
