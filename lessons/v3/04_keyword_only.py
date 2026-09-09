"""V3-04 参数顺序与 keyword-only 参数。

学习目标：
1. 记住常见参数顺序：普通位置参数 → 默认参数 → *args → keyword-only → **kwargs。
2. 理解单独一个 * 的含义：后面的参数必须用关键字传递。
3. 能看懂 def create_user(name: str, *, active: bool = True) 这种库 API 签名。

运行：uv run python lessons/v3/04_keyword_only.py
"""


# ---------------------------------------------------------------------------
# 先看最普通的：位置参数 + 默认参数。
# greeting 可以不传；name 必须传。
# ---------------------------------------------------------------------------
def greet(name: str, greeting: str = "Hi") -> str:
    """普通默认参数。greeting 既可以按位置传，也可以按关键字传。"""
    return f"{greeting}, {name}"


print(greet("Tom"))
print(greet("Tom", "Hello"))
print(greet("Tom", greeting="Hello"))


# ---------------------------------------------------------------------------
# keyword-only：* 后面的参数只能用关键字传入。
# 参数：name 位置或关键字都行；active 必须写成 active=...
# 返回：一个小 dict。
# 注意：create_user("Tom", True) 会 TypeError，因为 True 被当成了多余位置参数。
# JS/TS 对比：TS 没有 keyword-only。前端常用 options 对象强制「按名字传」。
# 后续 FastAPI / Pydantic / SQLAlchemy 中会经常出现这种「必须写参数名」的签名。
# ---------------------------------------------------------------------------
def create_user(name: str, *, active: bool = True) -> dict:
    """active 是 keyword-only，调用时必须写 active=..."""
    return {"name": name, "active": active}


print("create_user('Tom') =", create_user("Tom"))
print("create_user('Tom', active=False) =", create_user("Tom", active=False))
# create_user("Tom", False)  # 注意：这行会报错，不要取消注释硬跑。


# ---------------------------------------------------------------------------
# 单独的 * 不收集任何位置参数，只负责「切开」：后面全部 keyword-only。
# timeout / ssl 都必须写名字，避免调用方搞混两个 bool/int 的含义。
# ---------------------------------------------------------------------------
def connect(host: str, *, timeout: int = 30, ssl: bool = True) -> str:
    """模拟常见库 API：必填位置参数 + 一堆必须写名字的选项。"""
    return f"connect {host} timeout={timeout} ssl={ssl}"


print(connect("localhost"))
print(connect("localhost", timeout=5, ssl=False))


# ---------------------------------------------------------------------------
# *args 后面的参数也自动变成 keyword-only。
# 不要一次记太复杂的签名；看到时按「* 之后必须写名字」理解即可。
# ---------------------------------------------------------------------------
def search(query: str, *tags: str, limit: int = 10) -> dict:
    """query 和 tags 按位置；limit 必须写 limit=。"""
    return {"query": query, "tags": tags, "limit": limit}


print("search 默认 limit =", search("python", "backend", "fastapi"))
print("search 指定 limit =", search("python", "backend", limit=2))

if __name__ == "__main__":
    print("\n--- 04 keyword-only 运行完毕 ---")

# 本文件重点：
# 1. 常见顺序：位置参数 → 默认参数 → *args → keyword-only → **kwargs。
# 2. def f(name, *, active=True) 里的 * 表示后面必须写关键字。
# 3. 库用这种写法，是为了防止 create_user("Tom", False) 这种看不出含义的调用。
# 4. 先求看懂签名，不必自己设计很复杂的参数列表。
