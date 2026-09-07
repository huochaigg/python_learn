"""V1-02 类型：常用内置类型、查看类型、类型转换。

运行：uv run python lessons/v1_basics/02_types.py
"""

# 常用内置类型
n = 10          # int  整数
f = 3.14        # float 浮点数
s = "hello"     # str  字符串
b = True        # bool 布尔（只有 True / False）
z = None        # NoneType 表示“没有值”

print("type(n) =", type(n), n)
print("type(f) =", type(f), f)
print("type(s) =", type(s), s)
print("type(b) =", type(b), b)
print("type(z) =", type(z), z)

# 字符串常用操作
print("拼接:", s + " world")
print("重复:", s * 2)
print("长度:", len(s))
print("切片 s[1:4] =", s[1:4])

# 类型转换：把一种类型变成另一种（可能失败，例如 int("abc")）
print("int('42') =", int("42"))
print("float('3.5') =", float("3.5"))
print("str(100) =", str(100))
print("bool(0) =", bool(0), "bool(1) =", bool(1), "bool('') =", bool(""))

# 算术：/ 永远得到 float；// 整除；% 取余；** 幂
print("7 / 2 =", 7 / 2)
print("7 // 2 =", 7 // 2)
print("7 % 2 =", 7 % 2)
print("2 ** 10 =", 2 ** 10)

if __name__ == "__main__":
    print("\n--- 02 类型 运行完毕 ---")
