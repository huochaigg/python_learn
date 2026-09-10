"""V7-03 实例属性 vs 类属性。

学习目标：
1. 分清 self.xxx（实例）和写在 class 里的共享属性。
2. 会用 User.species 和 user.species 两种读法。
3. 观察「实例赋值同名属性」会盖住类属性。

运行：uv run python lessons/v7/03_instance_class_attributes.py
"""


class User:
    # 类属性：写在 class 里、不在 __init__ 里。
    # 用途：所有实例共享的数据，类似「类级默认值」。
    # JS/TS 对比：有点像 static property，但不完全等同。
    # 读取：User.species 或 user.species（实例上没有同名属性时）。
    species = "human"
    role = "user"

    def __init__(self, name: str) -> None:
        # 实例属性：属于某一个对象。
        # JS/TS 对比：this.name
        self.name = name


tom = User("Tom")
jack = User("Jack")

print("类上读 User.species =", User.species)
print("实例上读 tom.species =", tom.species)
print("jack.species =", jack.species)
print("实例属性互不影响:", tom.name, jack.name)

# 属性查找：先看实例，没有再到类上找。本课先记住现象，不深入 descriptor。
print("\n给 tom.role 赋值之后：")
tom.role = "admin"
print("tom.role =", tom.role)
print("jack.role 仍是类上的 =", jack.role)
print("User.role 仍是 =", User.role)
print("tom.__dict__（实例自己的数据）=", tom.__dict__)
print("jack.__dict__ =", jack.__dict__)

# ---------------------------------------------------------------------------
# 坑：不要用可变 list/dict 当类属性去存「每个实例自己的数据」。
# 所有实例会共享同一个 list，改一个等于改全家。
# 每个实例自己的列表应在 __init__ 里 self.items = []。
# 这和 V3「可变默认参数」是同一类坑。
# ---------------------------------------------------------------------------
class Cart:
    items: list[str] = []  # 错误示范：共享购物车


a = Cart()
b = Cart()
a.items.append("apple")
print("\n错误示范：a 加一件后，b.items =", b.items)

class GoodCart:
    def __init__(self) -> None:
        self.items = []


c = GoodCart()
d = GoodCart()
c.items.append("apple")
print("正确示范：c 加一件后，d.items =", d.items)

if __name__ == "__main__":
    print("\n--- 03 实例属性 / 类属性 运行完毕 ---")

# 本文件重点：
# 1. self.xxx 通常是实例属性；class 里直接赋值的是类属性。
# 2. 读取时先看实例，再看类。
# 3. tom.role = "admin" 只给 tom 盖了一层，不会改 User.role。
# 4. 可变 list/dict 不要当「每个实例一份」的类属性。
