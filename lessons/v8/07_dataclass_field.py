"""V8-07 dataclass 默认值与 field(default_factory=list)。

学习目标：
1. 不可变默认值可以直接写 active: bool = True。
2. list/dict/set 要用 field(default_factory=list)，否则会共享。
3. 把这个坑和 V3 可变默认参数联系起来。

运行：uv run python lessons/v8/07_dataclass_field.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    active: bool = True
    # field(default_factory=list)
    # 是什么：告诉 dataclass「每个实例都调用一次 list() 当默认值」。
    # 什么时候用：默认值是 list / dict / set 等可变对象。
    # 返回/效果：每个 User() 拿到自己的新 list，互不影响。
    # 坑：不要写 roles: list[str] = []，那是共享同一个 list。
    # 这和 V3 的 def add_item(items=[]) 是同一类问题。
    roles: list[str] = field(default_factory=list)


tom = User("Tom")
ada = User("Ada")
tom.roles.append("editor")
print("tom.roles =", tom.roles)
print("ada.roles 仍是空 =", ada.roles)
print("tom.active 默认 True =", tom.active)


# 错误示范：可变默认值写在 class 字段上（不要学）。
class BadUser:
    roles: list[str] = []


bad_a = BadUser()
bad_b = BadUser()
bad_a.roles.append("admin")
print("错误示范：bad_a 加角色后 bad_b.roles =", bad_b.roles)

if __name__ == "__main__":
    print("\n--- 07 dataclass field 运行完毕 ---")

# 本文件重点：
# 1. bool/int/str/None 这类不可变默认值可以直接写。
# 2. 可变默认字段用 field(default_factory=list)。
# 3. default_factory 会为每个实例单独创建对象。
# 4. 和 V3「默认参数不要用 []」是同一个坑。
