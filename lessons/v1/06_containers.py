"""V1-06 容器：list / tuple / dict / set。

运行：uv run python lessons/v1_basics/06_containers.py
"""

# list：有序、可变、可重复
nums = [3, 1, 2]
nums.append(4)
nums.sort()
print("list:", nums, "nums[0] =", nums[0])

# 列表推导：用一行从已有序列生成新列表
squares = [x * x for x in nums if x % 2 == 0]
print("偶数的平方:", squares)

# tuple：有序、不可变（适合当“固定一组值”）
point = (10, 20)
print("tuple:", point, "x =", point[0])

# dict：键值对，键必须可哈希（常用 str / int）
user = {"name": "Ada", "age": 28}
user["city"] = "Shanghai"
print("dict:", user)
print("user['name'] =", user["name"])
print("keys:", list(user.keys()), "values:", list(user.values()))

# set：无序、不重复，适合去重和集合运算
a = {1, 2, 3, 3}
b = {3, 4}
print("set a =", a)
print("并集:", a | b, "交集:", a & b, "差集:", a - b)

# 遍历 dict
for key, value in user.items():
    print(f"  {key} -> {value}")

for key, value in enumerate[str](user):
    print(f"  {key} -> {value}")

if __name__ == "__main__":
    print("\n--- 06 容器 运行完毕 ---")
