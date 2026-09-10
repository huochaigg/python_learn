"""V8-03 @staticmethod：领域相关、但不碰 self/cls 的纯函数。

学习目标：
1. 会把校验逻辑写成 staticmethod。
2. 知道它只是「放在类命名空间里的普通函数」。
3. 需要实例状态时不要硬写成 staticmethod。

运行：uv run python lessons/v8/03_staticmethod.py
"""


class User:
    def __init__(self, name: str, age: int, email: str) -> None:
        self.name = name
        self.age = age
        self.email = email

    @staticmethod
    def is_valid_age(age: int) -> bool:
        # @staticmethod：不会自动传入实例或类。
        # 用途：逻辑属于 User 这个领域，但计算过程不读 self，也不读 cls。
        # 调用：User.is_valid_age(31) 或 user.is_valid_age(31)，两种都能跑。
        # 返回：本例是 bool，不修改任何对象状态。
        # JS/TS 对比：≈ static isValidAge(age: number): boolean
        return age >= 0

    @staticmethod
    def is_valid_email(email: str) -> bool:
        # 极简演示，不是完整邮箱校验。
        return "@" in email and "." in email.split("@")[-1]

    def describe(self) -> str:
        # 需要 self.email / self.age → 必须是实例方法。
        # 注意：不要为了「看起来整齐」把 describe 改成 staticmethod。
        return f"{self.name} <{self.email}> age={self.age}"


print("User.is_valid_age(31) =", User.is_valid_age(31))
print("User.is_valid_age(-1) =", User.is_valid_age(-1))
print("User.is_valid_email('a@b.com') =", User.is_valid_email("a@b.com"))
print("User.is_valid_email('nope') =", User.is_valid_email("nope"))

tom = User("Tom", 31, "tom@example.com")
print("实例方法 describe =", tom.describe())
print("也可以从实例调静态方法 =", tom.is_valid_age(18))

# 如果校验和 User 领域关系不强，写成模块级函数也完全可以：
# def is_valid_age(age: int) -> bool: ...
# 不必为了演示把所有辅助函数都塞进 class。

if __name__ == "__main__":
    print("\n--- 03 staticmethod 运行完毕 ---")

# 本文件重点：
# 1. staticmethod ≈ TS static：不自动拿 self/cls。
# 2. 适合纯校验、纯格式化，逻辑上属于这个类。
# 3. 要用到 self.xxx 就改回实例方法。
# 4. 不属于该类领域的工具函数，放模块顶层即可。
