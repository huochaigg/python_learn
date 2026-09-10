"""V8-01 三种方法对照：实例方法 / classmethod / staticmethod。

学习目标：
1. 在同一个 User 里看清 self、cls、以及「什么都不自动传」。
2. 记住判断原则：要实例状态 → 实例方法；要类本身/工厂 → classmethod；都不依赖 → staticmethod。
3. 能把它们粗略映射到 JS/TS，但知道 classmethod 是 Python 特有的「自动传类」。

运行：uv run python lessons/v8/01_instance_class_static.py
"""


class User:
    default_role = "user"

    def __init__(self, name: str, role: str | None = None) -> None:
        self.name = name
        self.role = role or User.default_role

    def activate_label(self) -> str:
        # 实例方法：第一个参数 self = 当前对象。
        # 适合：读/改这个对象的状态。调用：user.activate_label()
        # JS/TS 对比：普通实例方法，this 自动有；Python 必须把 self 写出来。
        return f"{self.name} is {self.role}"

    @classmethod
    def with_default_role(cls, name: str) -> "User":
        # @classmethod：装饰器，把函数变成「绑定在类上、自动传入类」的方法。
        # Python 会自动把当前类传给第一个参数，习惯叫 cls（class 的缩写）。
        # 适合：工厂方法、需要知道「现在是哪个类」的逻辑。
        # 调用：User.with_default_role("Tom")，不必先有实例。
        # JS/TS 对比：有点像 static factory，但 TS static 不会自动多收一个「类」参数。
        return cls(name, cls.default_role)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        # @staticmethod：放进类命名空间的普通函数。
        # 不会自动收到 self，也不会收到 cls。
        # 适合：和这个领域相关、但不碰实例/类状态的纯逻辑。
        # JS/TS 对比：≈ static isValidName(name: string)
        # 注意：如果其实需要 self.name，就不要硬写成 staticmethod。
        return len(name.strip()) >= 2


tom = User("Tom")
print("实例方法 =", tom.activate_label())
print("类方法工厂 =", User.with_default_role("Ada").activate_label())
print("静态方法校验 =", User.is_valid_name("A"), User.is_valid_name("Ada"))

# 判断原则（后面几课会反复用）：
# 需要当前实例状态 → 实例方法
# 需要类本身，或作为工厂创建实例 → classmethod
# 完全不依赖实例和类状态，只是逻辑上属于这个领域 → staticmethod
# 若辅助函数并不属于某个领域类，也可以直接写成模块级函数，不必硬塞进 class。

if __name__ == "__main__":
    print("\n--- 01 三种方法对照 运行完毕 ---")

# 本文件重点：
# 1. 实例方法自动传 self；classmethod 自动传 cls；staticmethod 什么都不自动传。
# 2. 先问「依赖实例、依赖类、还是谁都不依赖」，再选哪一种。
# 3. classmethod 比 TS static 多了一层「cls 是当前类」。
# 4. 不是所有函数都要塞进 class。
