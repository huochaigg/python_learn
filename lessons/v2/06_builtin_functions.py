"""V2-06 常用内置函数：len / sum / min / max / any / all。

学习目标：
1. 会用 len / sum / min / max 处理序列。
2. 理解 any() ≈ JS some()，all() ≈ JS every()。
3. 能结合推导式做「是否存在 / 是否全部满足」判断。

运行：uv run python lessons/v2/06_builtin_functions.py
"""

nums: list[int] = [3, 1, 4, 1, 5]
permissions: list[bool] = [False, False, True]
users: list[dict[str, str]] = [
    {"name": "Tom", "role": "user"},
    {"name": "Lucy", "role": "admin"},
    {"name": "Jack", "role": "user"},
]

# ---------------------------------------------------------------------------
# len：求长度。参数：容器或序列。返回：int。不修改原对象。
# JS/TS 对比：≈ arr.length / Object.keys(obj).length
# ---------------------------------------------------------------------------
print("len(nums) =", len(nums))
print("len(users) =", len(users))

# ---------------------------------------------------------------------------
# sum：求和。参数：可迭代的数字，可选 start。返回：数字。不修改原对象。
# JS/TS 对比：≈ arr.reduce((a, b) => a + b, 0)
# ---------------------------------------------------------------------------
print("sum(nums) =", sum(nums))

# ---------------------------------------------------------------------------
# min / max：最小 / 最大值。参数：可迭代对象，或多个参数。返回：那个极值元素。
# JS/TS 对比：≈ Math.min(...arr) / Math.max(...arr)
# 注意：空序列会抛 ValueError。
# ---------------------------------------------------------------------------
print("min(nums) =", min(nums))
print("max(nums) =", max(nums))
print("min(3, 1, 4) =", min(3, 1, 4))

# ---------------------------------------------------------------------------
# any：只要有一个元素为真就 True；全假或空序列则 False。
# 参数：可迭代对象。返回：bool。不修改原对象。
# JS/TS 对比：≈ arr.some(Boolean) 或 arr.some(x => x)
# ---------------------------------------------------------------------------
print("any(permissions) =", any(permissions))
print("any([]) =", any([]))

# ---------------------------------------------------------------------------
# all：所有元素都为真才 True；有一个假就 False。空序列是 True。
# JS/TS 对比：≈ arr.every(Boolean)
# 注意：all([]) 是 True（空列表没有「失败的元素」），和前端 every([]) === true 一样。
# ---------------------------------------------------------------------------
print("all(permissions) =", all(permissions))
print("all([True, True]) =", all([True, True]))
print("all([]) =", all([]))

# ---------------------------------------------------------------------------
# 实际例子：users 中是否存在 admin
# 下面这种 (xxx for xxx in ...) 叫生成器表达式。
# 这里先眼熟，后续版本再专门学习 Generator。
# 目前只需知道：any(...) 会依次看每个条件，遇到 True 就可以停。
# JS/TS 对比：users.some(u => u.role === "admin")
# ---------------------------------------------------------------------------
has_admin = any(user["role"] == "admin" for user in users)
print("是否存在 admin =", has_admin)

# 若更想先看熟悉的列表推导式，效果一样（会先生成一整张临时 list）：
has_admin_via_list = any([user["role"] == "admin" for user in users])
print("用列表推导式写 any =", has_admin_via_list)

# all：是否所有人都是 admin
everyone_is_admin = all(user["role"] == "admin" for user in users)
print("是否所有人都是 admin =", everyone_is_admin)

if __name__ == "__main__":
    print("\n--- 06 内置函数 运行完毕 ---")

# 本文件重点：
# 1. len / sum / min / max 是序列上的高频统计函数。
# 2. any ≈ JS some；all ≈ JS every；空列表时 all([]) 为 True。
# 3. any(x["role"] == "admin" for x in users) 用来做「是否存在」。
# 4. 生成器表达式先混个眼熟即可，不必本文件深挖。
