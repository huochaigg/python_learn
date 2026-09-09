"""V2-02 dict 进阶：读取、增改、遍历、update / pop / del。

学习目标：
1. 分清 user["key"] 和 user.get("key")。
2. 会用 keys / values / items 遍历。
3. 理解 items() + 解包，对应 JS 的 Object.entries。

运行：uv run python lessons/v2/02_dict_advanced.py
"""

user: dict[str, str | int] = {"name": "Tom", "age": 31}
print("初始 user =", user)

# ---------------------------------------------------------------------------
# 读取：user["name"]
# 参数：键。返回：对应的值。不修改原 dict。
# 注意：键不存在会抛 KeyError。
# JS/TS 对比：≈ user.name / user["name"]；JS 缺字段是 undefined，Python 会报错。
# ---------------------------------------------------------------------------
print('user["name"] =', user["name"])

# ---------------------------------------------------------------------------
# get：安全读取。参数：key，可选 default。返回：值或默认值。不修改原 dict。
# 缺键时：get("x") 得到 None；get("x", 默认值) 得到你给的默认值。
# JS/TS 对比：≈ user.name ?? default；比直接 [] 更接近前端习惯。
# ---------------------------------------------------------------------------
print('user.get("name") =', user.get("name"))
print('user.get("city") =', user.get("city"))
print('user.get("city", "unknown") =', user.get("city", "unknown"))

# ---------------------------------------------------------------------------
# 新增字段：赋值给一个还不存在的键。会修改原 dict。
# JS/TS 对比：user.city = "Shanghai"
# ---------------------------------------------------------------------------
user["city"] = "Shanghai"
print("新增 city 之后 =", user)

# ---------------------------------------------------------------------------
# 修改字段：赋值给已存在的键。会修改原 dict。
# JS/TS 对比：同样是赋值覆盖。
# ---------------------------------------------------------------------------
user["age"] = 32
print("修改 age 之后 =", user)

# ---------------------------------------------------------------------------
# keys：返回所有键的视图。不修改原 dict。
# JS/TS 对比：≈ Object.keys(user)
# 注意：dict_keys 不是 list，需要随机访问时再 list(...) 包一层。
# ---------------------------------------------------------------------------
print("keys() =", user.keys())
print("list(keys()) =", list(user.keys()))

# ---------------------------------------------------------------------------
# values：返回所有值的视图。不修改原 dict。
# JS/TS 对比：≈ Object.values(user)
# ---------------------------------------------------------------------------
print("values() =", list(user.values()))

# ---------------------------------------------------------------------------
# items：返回 (key, value) 对。不修改原 dict。
# JS/TS 对比：≈ Object.entries(user)  →  [["name", "Tom"], ["age", 32], ...]
# Python 每一项是 tuple：(key, value)
# ---------------------------------------------------------------------------
print("items() =", list(user.items()))

# ---------------------------------------------------------------------------
# 遍历 dict
# 只写 for key in user: 默认遍历的是 key（≈ Object.keys）
# for key, value in user.items(): 同时拿到键和值
# 这里用到了两件事：
#   1. dict.items() 产出一个个 (key, value) tuple
#   2. for key, value in ... 把这个二元 tuple 解包成两个变量
# JS/TS 对比：
#   for (const [key, value] of Object.entries(user)) { ... }
# ---------------------------------------------------------------------------
print("--- 只遍历 key ---")
for key in user:
    print("  key =", key)

print("--- items() + 解包 ---")
for key, value in user.items():
    print(f"  {key} -> {value}")

# ---------------------------------------------------------------------------
# update：把另一个 dict 的键值合并进来。参数：dict 或关键字参数。返回：None。
# 会修改原 dict；已有键会被覆盖。
# JS/TS 对比：≈ Object.assign(user, extra) 或 { ...user, ...extra } 但 update 是原地改。
# ---------------------------------------------------------------------------
user.update({"age": 33, "role": "admin"})
print("update 之后 =", user)

# ---------------------------------------------------------------------------
# pop：按键删除并返回值。参数：key，可选 default。会修改原 dict。
# 注意：没给 default 且键不存在 → KeyError。
# JS/TS 对比：没有同名；通常是 const v = user.x; delete user.x。
# ---------------------------------------------------------------------------
role = user.pop("role")
print("pop('role') 得到 =", role, "剩余 =", user)

# ---------------------------------------------------------------------------
# del：按键删除，不返回值。会修改原 dict。
# 注意：键不存在 → KeyError。
# JS/TS 对比：≈ delete user.city
# ---------------------------------------------------------------------------
del user["city"]
print("del city 之后 =", user)

if __name__ == "__main__":
    print("\n--- 02 dict 进阶 运行完毕 ---")

# 本文件重点：
# 1. [] 缺键抛 KeyError；get() 缺键返回 None 或默认值，更安全。
# 2. items() ≈ Object.entries()；for k, v in d.items() 是 items + 解包。
# 3. update / pop / del 都会改原 dict。
# 4. keys/values/items 返回的是视图，不是 list。
