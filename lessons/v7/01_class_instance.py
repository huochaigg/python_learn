"""V7-01 class 与实例：Python 没有 new。

学习目标：
1. 会定义最简单的 class，并创建多个实例。
2. 记住：JS 用 new User()，Python 用 User()。
3. 确认不同实例是不同对象。

运行：uv run python lessons/v7/01_class_instance.py
"""


# ---------------------------------------------------------------------------
# class：定义一类对象的模板。
# 用途：把「数据 + 以后要加的行为」收在一个类型里。
# JS/TS 对比：class User {} 概念完全一样。
# 坑：Python 创建实例没有 new。写成 new User() 会 NameError。
# ---------------------------------------------------------------------------
class User:
    """最瘦的用户类，本文件先不写方法和继承。"""


tom = User()
jack = User()

print("tom =", tom)
print("jack =", jack)
print("tom 和 jack 是同一个对象吗 =", tom is jack)
print("type(tom) =", type(tom))

# JS/TS 对比：
#   const tom = new User()
# Python：
#   tom = User()

if __name__ == "__main__":
    print("\n--- 01 class / 实例 运行完毕 ---")

# 本文件重点：
# 1. class User: 对应 JS class User。
# 2. 实例化：User()，不要写 new。
# 3. 每次 User() 都得到一个新对象。
# 4. 方法和继承下一课再加，先把「类 vs 实例」看清楚。
