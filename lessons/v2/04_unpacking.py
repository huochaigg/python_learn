"""V2-04 解包：tuple / list 解包、*rest、* 展开 list、** 展开 dict。

学习目标：
1. 掌握 x, y = point 这种位置解包。
2. 掌握 *rest 收集剩余项（对应 JS rest）。
3. 掌握 *list 展开、**dict 展开（对应 JS 展开语法）。
4. 理解 create_user(**user_data) 为什么后面会到处见到。

运行：uv run python lessons/v2/04_unpacking.py
"""


# ---------------------------------------------------------------------------
# 1. tuple 解包：右边有几个值，左边就写几个名字。
# JS/TS 对比：const [x, y] = point
# ---------------------------------------------------------------------------
point = (10, 20)
x, y = point
print("tuple 解包 x =", x, "y =", y)

# ---------------------------------------------------------------------------
# 2. list 解包：语法和 tuple 一样。
# 注意：左右个数必须一致，否则 ValueError。
# JS/TS 对比：const [a, b, c] = [1, 2, 3]
# ---------------------------------------------------------------------------
a, b, c = [1, 2, 3]
print("list 解包 a, b, c =", a, b, c)

# ---------------------------------------------------------------------------
# 3. *rest：把「剩下的」收成一个 list。
# JS/TS 对比：const [first, ...rest] = list
# 注意：Python 这边 rest 一定是 list；JS 的 rest 也是数组。
# ---------------------------------------------------------------------------
first, *rest = [1, 2, 3, 4]
print("first =", first, "rest =", rest)

# ---------------------------------------------------------------------------
# 4. 前后都解包：中间剩下的全部进 *middle。
# JS/TS 对比：JS 不能直接写 const [first, ...middle, last]，rest 只能在最后。
# 这是 Python 比 JS 更灵活的地方。
# ---------------------------------------------------------------------------
first, *middle, last = [1, 2, 3, 4, 5]
print("first =", first, "middle =", middle, "last =", last)

# ---------------------------------------------------------------------------
# 5. * 展开 list：把 list 里的元素「摊开」放到另一个 list / 函数参数里。
# JS/TS 对比：const result = [...a, ...b]
# ---------------------------------------------------------------------------
left = [1, 2]
right = [3, 4]
result = [*left, *right]
print("[*left, *right] =", result)

# 也可以摊进函数位置参数：print(*left) 相当于 print(1, 2)
print("*left 作为位置参数：", end=" ")
print(*left)

# ---------------------------------------------------------------------------
# 6. ** 展开 dict：把 dict 的键值对摊开成关键字参数，或摊进另一个 dict。
# JS/TS 对比：
#   const newUser = { ...user, age: 32 }
# 后面的键会覆盖前面的同名键，两边规则一样。
# ---------------------------------------------------------------------------
user = {
    "name": "Tom",
    "age": 31,
}
new_user = {
    **user,
    "age": 32,
}
print("原 user =", user)
print("new_user =", new_user)
# 注意：这是浅拷贝 + 覆盖。改 new_user 不会改 user 的顶层字段。

# ---------------------------------------------------------------------------
# 7. **dict 传给函数：这是后端代码里极高频的写法。
#
# **user_data 会把
#   {"name": "Tom", "age": 31}
# 转换成关键字参数
#   name="Tom", age=31
#
# 所以下面两行完全等价：
#   create_user(name="Tom", age=31)
#   create_user(**user_data)
#
# 后续 FastAPI 中会经常出现：
#   User(**data)            # Pydantic 用 dict 构造模型
#   db.execute(stmt, **params)
#   return {**old, **patch} # 合并更新字段
# ---------------------------------------------------------------------------
def create_user(name: str, age: int) -> str:
    return f"{name} is {age}"


user_data = {
    "name": "Tom",
    "age": 31,
}

print("create_user(**user_data) =", create_user(**user_data))
print("显式写出关键字参数 =", create_user(name="Tom", age=31))

# 注意：
# - dict 的 key 必须和函数参数名对得上，多了或少了都会 TypeError。
# - JS 没有「把对象摊成函数命名参数」这种内置语法，通常是 createUser(userData)。

if __name__ == "__main__":
    print("\n--- 04 解包 运行完毕 ---")

# 本文件重点：
# 1. x, y = point 是位置解包；个数必须对齐。
# 2. *rest ≈ JS 的 ...rest；Python 还允许 first, *middle, last。
# 3. *list 展开序列；**dict 展开成关键字参数或新 dict。
# 4. create_user(**data) 在 FastAPI / Pydantic 里会反复出现，先记熟形态。
