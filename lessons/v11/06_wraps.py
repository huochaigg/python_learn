"""V11-06 functools.wraps：保留原函数的 __name__ / __doc__。

学习目标：
1. 看到不加 wraps 时，__name__ 会变成 wrapper。
2. 加上 @wraps(func) 后元信息还在。
3. 知道正式 decorator 通常都应该 wraps。

运行：uv run python lessons/v11/06_wraps.py
"""

from functools import wraps


def without_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def with_wraps(func):
    # functools.wraps(func)：把原函数的 __name__、__doc__ 等 metadata 复制到 wrapper 上。
    # 用途：调试、文档、框架自省时仍看到「业务函数名」，而不是 wrapper。
    # 输入：被装饰的原函数；作用在 wrapper 上。
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def hello() -> str:
    """打个招呼。"""
    return "hi"


print("原函数 __name__ =", hello.__name__)
print("原函数 __doc__ =", hello.__doc__)

lost = without_wraps(hello)
print("\n不用 wraps: __name__ =", lost.__name__, "__doc__ =", lost.__doc__)

kept = with_wraps(hello)
print("使用 wraps: __name__ =", kept.__name__, "__doc__ =", kept.__doc__)

if __name__ == "__main__":
    print("\n--- 06 wraps 运行完毕 ---")

# 本文件重点：
# 1. 不加 wraps，对外名字往往变成 wrapper。
# 2. @wraps(func) 保留 __name__ / __doc__ 等。
# 3. 正式 decorator 默认都加 wraps。
# 4. 框架、调试、文档生成会依赖这些元信息。
