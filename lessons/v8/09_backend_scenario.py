"""V8-09 后端小场景：组合 classmethod / staticmethod / property / dataclass。

学习目标：
1. 用 dataclass 定义 User，用普通 class 给 Order 做 qty setter。
2. 工厂创建管理员、静态方法校验、property 算展示名和总价。
3. 仍然只在内存里模拟，不引入 FastAPI 或数据库。

运行：uv run python lessons/v8/09_backend_scenario.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    role: str = "user"
    active: bool = True
    permissions: list[str] = field(default_factory=list)

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return len(name.strip()) >= 2

    @classmethod
    def create_admin(cls, name: str) -> "User":
        if not cls.is_valid_name(name):
            raise ValueError("invalid name")
        return cls(name=name.strip().title(), role="admin", permissions=["users:write"])

    @property
    def display_name(self) -> str:
        prefix = "Admin" if self.role == "admin" else "User"
        return f"{prefix} {self.name}"


class Order:
    """qty 用 property setter 校验；total 是计算属性。

    注意：dataclass 字段和同名 @property 叠在一起容易打架，
    需要 setter 的字段用普通 class 更直观。
    """

    def __init__(self, user: User, unit_price: int, qty: int = 1) -> None:
        self.user = user
        self.unit_price = unit_price
        self.tags: list[str] = []
        self.qty = qty

    @property
    def qty(self) -> int:
        return self._qty

    @qty.setter
    def qty(self, value: int) -> None:
        if value <= 0:
            raise ValueError("qty must be > 0")
        self._qty = value

    @property
    def total(self) -> int:
        return self.unit_price * self.qty


admin = User.create_admin("  ada  ")
print("create_admin =", admin)
print("display_name =", admin.display_name)

order = Order(user=admin, unit_price=50, qty=3)
order.tags.append("vip")
print("order.total =", order.total)
print("order.tags =", order.tags)

try:
    order.qty = 0
except ValueError as e:
    print("setter 拒绝非法 qty =", e)

try:
    User.create_admin("x")
except ValueError as e:
    print("工厂拒绝非法名字 =", e)

if __name__ == "__main__":
    print("\n--- 09 后端场景 运行完毕 ---")

# 本文件重点：
# 1. 工厂 → classmethod；纯校验 → staticmethod；展示名/总价 → property。
# 2. dataclass + field(default_factory=list) 保存 permissions。
# 3. 需要 setter 的 qty 放普通 class，避免和 dataclass 字段同名冲突。
# 4. 这是 V7+V8 的组合，还不是 FastAPI。
