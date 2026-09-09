"""V2-07 综合练习：把 V1（for / if / dict）和 V2（推导式 / set / 解包 / any all）串起来。

学习目标：
1. 独立完成下面 10 个小练习。
2. 先在 TODO 区域自己写，再往下看示例答案。
3. 打断点对比你的变量和示例答案。

运行：uv run python lessons/v2/07_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

users: list[dict[str, int | str | bool]] = [
    {
        "id": 1,
        "name": "Tom",
        "age": 31,
        "role": "admin",
        "active": True,
    },
    {
        "id": 2,
        "name": "Jack",
        "age": 17,
        "role": "user",
        "active": False,
    },
    {
        "id": 3,
        "name": "Lucy",
        "age": 25,
        "role": "user",
        "active": True,
    },
    {
        "id": 4,
        "name": "Mike",
        "age": 20,
        "role": "admin",
        "active": True,
    },
]


# =============================================================================
# 练习 1
# TODO: 遍历所有用户，把每个 user 打印出来。
# JS/TS 对比：users.forEach(user => console.log(user))
# =============================================================================
print("\n===== 练习 1 TODO =====")
print("users in users =", [user2 for user2 in users])

print("===== 练习 1 示例答案 =====")
for user in users:
    print(user)


# =============================================================================
# 练习 2
# TODO: 找出所有成年人（age >= 18），放进一个新 list，再打印。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")
adults: list[dict[str, int | str | bool]] = []
for user in users:
    if user["age"] >= 18:
        adults.append(user)
print("adults =", adults)


# =============================================================================
# 练习 3
# TODO: 使用列表推导式得到成年人的 name，例如 ["Tom", "Lucy", "Mike"]。
# JS/TS 对比：users.filter(u => u.age >= 18).map(u => u.name)
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")
adult_names = [user["name"] for user in users if user["age"] >= 18]
print("adult_names =", adult_names)


# =============================================================================
# 练习 4
# TODO: 使用 set 得到所有不同 role。
# JS/TS 对比：new Set(users.map(u => u.role))
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")
roles = {user["role"] for user in users}
print("roles =", roles)


# =============================================================================
# 练习 5
# TODO: 创建 {"Tom": 31, "Jack": 17, ...} 这样的 dict。
# JS/TS 对比：Object.fromEntries(users.map(u => [u.name, u.age]))
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")
name_to_age = {user["name"]: user["age"] for user in users}
print("name_to_age =", name_to_age)


# =============================================================================
# 练习 6
# TODO: 使用 any() 判断是否存在 admin。
# JS/TS 对比：users.some(u => u.role === "admin")
# =============================================================================
print("\n===== 练习 6 TODO =====")


print("===== 练习 6 示例答案 =====")
has_admin = any(user["role"] == "admin" for user in users)
print("has_admin =", has_admin)


# =============================================================================
# 练习 7
# TODO: 使用 all() 判断是否所有用户都 active。
# JS/TS 对比：users.every(u => u.active)
# =============================================================================
print("\n===== 练习 7 TODO =====")


print("===== 练习 7 示例答案 =====")
all_active = all(user["active"] for user in users)
print("all_active =", all_active)


# =============================================================================
# 练习 8
# TODO: 基于 users[0]，用 **user 创建一个新 dict：
#       - 修改 age 为 99
#       - 不修改原 user
# JS/TS 对比：const newUser = { ...user, age: 99 }
# 后续 FastAPI 中会经常出现：用 **data 合并更新字段。
# =============================================================================
print("\n===== 练习 8 TODO =====")


print("===== 练习 8 示例答案 =====")
tom = users[0]
tom_updated = {
    **tom,
    "age": 99,
}
print("新数据 tom_updated =", tom_updated)
print("原 user 未被修改 =", tom)


# =============================================================================
# 练习 9
# TODO: 从 adult_names 里解包出 first / middle / last。
# 提示：first, *middle, last = adult_names
# JS/TS 对比：JS 的 rest 只能写在最后，不能直接拆出 last。
# =============================================================================
print("\n===== 练习 9 TODO =====")


print("===== 练习 9 示例答案 =====")
first, *middle, last = adult_names
print("first =", first, "middle =", middle, "last =", last)


# =============================================================================
# 练习 10
# TODO: 把上面得到的关键结果打印成一份摘要。
#       至少包括：adult_names / roles / name_to_age / has_admin / all_active
# =============================================================================
print("\n===== 练习 10 TODO =====")


print("===== 练习 10 示例答案 =====")
print("---------- 处理结果 ----------")
print("adult_names =", adult_names)
print("roles =", roles)
print("name_to_age =", name_to_age)
print("has_admin =", has_admin)
print("all_active =", all_active)
print("tom_updated =", tom_updated)
print("unpack first/middle/last =", first, middle, last)

if __name__ == "__main__":
    print("\n--- 07 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 普通 for + if 能做的过滤，推导式通常也能做，先写懂再压缩。
# 2. set / dict comprehension 适合去重和「名字 → 年龄」这种映射。
# 3. any / all 用来做存在性和全称判断，对应 JS 的 some / every。
# 4. **user 做浅拷贝更新，原 dict 保持不变。
# 5. first, *middle, last 是 Python 特有的前后解包。
