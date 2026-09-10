"""V8-06 @dataclass：少写样板，但仍是真正的 class。

学习目标：
1. 对比手写 __init__ 和 @dataclass 版本。
2. 看到自动生成的 __init__、__repr__、__eq__。
3. 记住 dataclass ≠ TypeScript interface（运行时真的存在、能实例化）。

运行：uv run python lessons/v8/06_dataclass.py
"""

from dataclasses import dataclass


class PlainUser:
    """普通 class：数据类常常要手写初始化和展示。"""

    def __init__(self, name: str, age: int, active: bool = True) -> None:
        self.name = name
        self.age = age
        self.active = active

    def __repr__(self) -> str:
        return f"PlainUser(name={self.name!r}, age={self.age}, active={self.active})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlainUser):
            return NotImplemented
        return (self.name, self.age, self.active) == (other.name, other.age, other.active)


# ---------------------------------------------------------------------------
# @dataclass：标准库装饰器，按类型标注的字段自动生成常见样板方法。
# 自动提供：__init__、__repr__、__eq__ 等（本课先用到这几个）。
# 它仍然是真正的 Python class：能 User(...)、能写方法、能继承。
# JS/TS 对比：不是 interface（interface 运行时消失）。更接近「少写样板的数据类」。
# 后面 FastAPI 的 Pydantic BaseModel 看起来很像，但职责是校验/解析/DTO，不要混为一谈。
# ---------------------------------------------------------------------------
@dataclass
class User:
    name: str
    age: int
    active: bool = True

    def label(self) -> str:
        return f"{self.name} ({self.age})"


plain = PlainUser("Tom", 31)
data = User("Tom", 31)
print("手写 repr =", plain)
print("dataclass repr =", data)
print("dataclass 仍可调用方法 =", data.label())

print("字段相同则 == :", User("Tom", 31) == User("Tom", 31))
print("手写版同样可比较 =", PlainUser("Tom", 31) == PlainUser("Tom", 31))
print("type(data) =", type(data))

if __name__ == "__main__":
    print("\n--- 06 dataclass 运行完毕 ---")

# 本文件重点：
# 1. dataclass 帮你省掉 __init__ / __repr__ / __eq__ 这类样板。
# 2. 它是真 class，不是 TS interface。
# 3. 字段用类型标注声明，默认值写在字段后面。
# 4. 和 Pydantic 长得像，但现在先当「数据对象快捷写法」。
