"""V1-03 条件：if / elif / else、比较与逻辑运算。

运行：uv run python lessons/v1_basics/03_conditionals.py
"""

score = 86

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "D"

print(f"分数 {score} -> 等级 {grade}")

# 比较：== != < <= > >=
# 逻辑：and / or / not
age = 20
has_ticket = True
if age >= 18 and has_ticket:
    print("可以入场")
else:
    print("不能入场")

# 三元表达式：条件成立取左边，否则取右边
status = "成年" if age >= 18 else "未成年"
print("status =", status)

# 成员判断
lang = "python"
if "py" in lang:
    print("'py' 在", lang, "里")

# 空值 / 假值：0, "", [], None, False 在 if 里都当作 False
value = ""
if not value:
    print("value 为空")

if __name__ == "__main__":
    print("\n--- 03 条件 运行完毕 ---")
