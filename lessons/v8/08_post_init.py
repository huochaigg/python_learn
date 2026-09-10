"""V8-08 __post_init__：自动 __init__ 跑完后再校验/补逻辑。

学习目标：
1. 知道 dataclass 生成 __init__ 之后会调用 __post_init__。
2. 能在里面做 age < 0 这类校验。
3. 不展开 dataclass 怎么生成方法。

运行：uv run python lessons/v8/08_post_init.py
"""

from dataclasses import dataclass, field


@dataclass
class User:
    name: str
    age: int
    roles: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # __post_init__：dataclass 自动生成的 __init__ 给字段赋值之后调用。
        # 用途：校验、派生字段、规范化输入。
        # 什么时候用：还想在「构造完成」时做事，但自己不再手写整个 __init__。
        # 坑：这里 raise 会让 User(...) 直接失败，和手写 __init__ 里校验一样。
        if self.age < 0:
            raise ValueError("age must be >= 0")
        self.name = self.name.strip().title()


print(User("  tom  ", 31))

try:
    User("Jack", -1)
except ValueError as e:
    print("构造失败 =", e)

if __name__ == "__main__":
    print("\n--- 08 __post_init__ 运行完毕 ---")

# 本文件重点：
# 1. dataclass 先自动填字段，再调用 __post_init__。
# 2. 适合校验和轻度规范化，不要在这里做 IO。
# 3. 非法数据直接 raise，调用方 try/except。
# 4. 底层代码生成机制本课不需要知道。
