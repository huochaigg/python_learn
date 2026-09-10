"""V8-02 @classmethod：工厂方法，内部用 cls(...) 而不是写死类名。

学习目标：
1. 会写 create_admin / from_dict 这类工厂。
2. 理解 cls 指向「调用时的那个类」，所以继承时更灵活。
3. 知道什么时候该用 classmethod：需要类本身来创建实例。

运行：uv run python lessons/v8/02_classmethod_factory.py
"""


class User:
    def __init__(self, name: str, role: str, active: bool = True) -> None:
        self.name = name
        self.role = role
        self.active = active

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, role={self.role!r})"

    @classmethod
    def create_admin(cls, name: str) -> "User":
        # @classmethod：调用 User.create_admin("Ada") 时，Python 自动传入 User 给 cls。
        # cls：当前类对象本身，不是实例。AdminUser.create_admin() 时 cls 就是 AdminUser。
        # 返回：一个实例。会修改/创建对象，但不改调用方已有的别的实例。
        # 坑：工厂里不要写死 User(...)，否则子类调用时仍造出父类实例。
        return cls(name, role="admin")

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        """从 dict 构造，后面 Pydantic/ORM 里 from_xxx / parse_xxx 很常见。"""
        return cls(name=data["name"], role=data.get("role", "user"))


class AdminUser(User):
    def grant(self, permission: str) -> str:
        return f"{self.name} granted {permission}"


print("User.create_admin =", User.create_admin("Ada"))
print("User.from_dict =", User.from_dict({"name": "Tom"}))

# 因为工厂用的是 cls(...)，子类调用时造出来的是 AdminUser，不是 User。
admin = AdminUser.create_admin("Root")
print("AdminUser.create_admin 的类型 =", type(admin).__name__, admin)
print(admin.grant("users:write"))

if __name__ == "__main__":
    print("\n--- 02 classmethod 工厂 运行完毕 ---")

# 本文件重点：
# 1. classmethod 自动获得 cls，指向「被点出来的那个类」。
# 2. 工厂方法内部用 cls(...)，继承时才不会写死父类。
# 3. create_xxx / from_xxx 是 classmethod 最常见的形态。
# 4. 需要改某个已有对象的字段时，用实例方法，不要用 classmethod。
