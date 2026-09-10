"""V8-04 @property：方法逻辑，属性式访问。

学习目标：
1. 会写 @property getter，用 user.full_name 而不是 user.full_name()。
2. 对照普通 get_full_name()，看清只是访问语法变了。
3. 知道 getter 里不要藏网络请求等重副作用。

运行：uv run python lessons/v8/04_property.py
"""


class User:
    def __init__(self, first_name: str, last_name: str) -> None:
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        """普通实例方法，调用时要加括号。"""
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        # @property：把方法伪装成属性（getter）。
        # 用途：计算属性。full_name 不必单独存，由 first/last 推导。
        # 调用：user.full_name  注意没有括号。
        # 返回：方法的返回值。本例不修改实例状态。
        # JS/TS 对比：get fullName() { return `${this.firstName} ${this.lastName}` }
        # 坑：看起来像字段，每次访问其实都会执行函数。不要在 getter 里发 HTTP / 查库。
        return f"{self.first_name} {self.last_name}"


user = User("Tom", "Hardy")
print("方法调用 get_full_name() =", user.get_full_name())
print("属性访问 full_name    =", user.full_name)
print("改 last_name 后再读 full_name =", end=" ")
user.last_name = "Holland"
print(user.full_name)

if __name__ == "__main__":
    print("\n--- 04 property 运行完毕 ---")

# 本文件重点：
# 1. @property 让方法用起来像属性：user.full_name，不要加 ()。
# 2. 适合由已有字段算出来的值，不必再存一份。
# 3. 访问时会跑函数，别把耗时副作用藏进 getter。
# 4. 和 JS getter 几乎是同一类需求。
