"""V1-01 变量：赋值、命名、解包。

运行：uv run python lessons/v1_basics/01_variables.py
"""

# 变量：名字指向一个值。Python 没有单独的“声明”，赋值即创建。
name = "Ada"
age = 28
height = 1.65
is_student = True

print("基本赋值:", name, age, height, is_student)

# 可以多次赋值，后一次会覆盖前一次（名字指向新值）
age = 29
print("重新赋值后 age =", age)

# 多重赋值、解包
x, y = 1, 2
print("解包:", x, y)
x, y = y, x
print("交换后:", x, y)

# 约定：全大写表示“不要改”的常量（语言层面并不强制）
PI = 3.14159
print("常量约定 PI =", PI)

# 命名：字母/数字/下划线，不能以数字开头；区分大小写
user_name = "bob"
User_name = "alice"
print("大小写不同:", user_name, User_name)

if __name__ == "__main__":
    print("\n--- 01 变量 运行完毕 ---")
