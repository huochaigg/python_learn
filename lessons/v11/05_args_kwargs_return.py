"""V11-05 wrapper(*args, **kwargs) 和返回值。

学习目标：
1. 用 *args/**kwargs 兼容无参、位置参、关键字参。
2. 看到忘记 return 时结果变成 None。
3. 把 V3 的收集/展开串回来。

运行：uv run python lessons/v11/05_args_kwargs_return.py
"""

from functools import wraps


def log_call(func):
    print(f"[定义阶段] 装饰 {func.__name__}")

    @wraps(func)
    def wrapper(*args, **kwargs):
        # wrapper 常用 *args, **kwargs：原函数无论什么签名都能接住。
        # 定义时收集；调用原函数时展开：func(*args, **kwargs)
        print(f"[调用阶段] {func.__name__} args={args} kwargs={kwargs}")
        return func(*args, **kwargs)

    return wrapper


@log_call
def ping() -> str:
    return "pong"


@log_call
def add(a: int, b: int) -> int:
    return a + b


@log_call
def greet(name: str, title: str = "Mr") -> str:
    return f"{title} {name}"


print("无参 =", ping())
print("位置参 =", add(2, 3))
print("关键字参 =", greet(name="Tom", title="Dr"))


def broken_decorator(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        # 错误：没有 return。原函数即使有返回值，外面拿到的也是 None。

    return wrapper


def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapper


def answer() -> str:
    return "42"


print("忘记 return =", broken_decorator(answer)())
print("正确 return =", good_decorator(answer)())

if __name__ == "__main__":
    print("\n--- 05 args/kwargs/返回值 运行完毕 ---")

# 本文件重点：
# 1. wrapper(*args, **kwargs) 再 func(*args, **kwargs)，才能装饰各种签名。
# 2. 有返回值的函数必须把结果 return 出去。
# 3. 漏 return 是 decorator 最常见的坑之一。
# 4. 这就是 V3「定义时收集、调用时展开」。
