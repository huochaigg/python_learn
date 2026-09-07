"""V1-07 综合练习：list + dict + for + if / elif + and + f-string。

运行：uv run python lessons/v1/07_Comprehensive.py
"""

users = [
    {"name": "Tom", "age": 31, "role": "admin"},
    {"name": "Jack", "age": 17, "role": "user"},
    {"name": "Lucy", "age": 25, "role": "user"},
]

for user in users:
    name = user["name"]
    age = user["age"]
    role = user["role"]

    if age >= 18 and role == "admin":
        print(f"{name} is adult admin")
    elif age >= 18:
        print(f"{name} is adult user")
    else:
        print(f"{name} is child")

if __name__ == "__main__":
    print("\n--- 07 综合练习 运行完毕 ---")
