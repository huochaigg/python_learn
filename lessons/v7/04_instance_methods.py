"""V7-04 实例方法：读属性、改状态、返回值。

学习目标：
1. 会写带 self 的实例方法，并用类型标注。
2. 能在方法里改 self.xxx。
3. 认识 _internal 表示「内部约定」，不是严格 private。

运行：uv run python lessons/v7/04_instance_methods.py
"""


class User:
    def __init__(self, name: str, active: bool = False) -> None:
        self.name = name
        self.active = active
        # _xxx：约定「内部使用，外面最好别随便碰」。
        # 注意：这不是 TS 的 private，外面 technically 仍能访问。
        self._notes = "internal"

    def get_name(self) -> str:
        """读取实例属性。"""
        return self.name

    def change_name(self, name: str) -> None:
        # -> None：这个方法没有有用的返回值，类似 TS 的 : void。
        # JS/TS 对比：changeName(name: string): void { this.name = name }
        self.name = name

    def activate(self) -> None:
        """修改当前实例状态。"""
        self.active = True


tom = User("Tom")
print("初始 =", tom.get_name(), "active =", tom.active)
tom.change_name("Thomas")
tom.activate()
print("改之后 =", tom.get_name(), "active =", tom.active)
print("约定上的内部字段 _notes =", tom._notes)

# 调用时不要写成 tom.activate(tom)。
# 定义时如果忘了 self：def activate(): ...
# 那么 tom.activate() 会 TypeError：把实例塞进了一个「不收参数」的函数。

if __name__ == "__main__":
    print("\n--- 04 实例方法 运行完毕 ---")

# 本文件重点：
# 1. 实例方法第一个参数是 self；调用 tom.activate() 时自动传入。
# 2. 方法里改 self.xxx，只影响当前实例。
# 3. -> None 类似 TS void。
# 4. _notes 只是约定内部使用，不是语言级 private。
