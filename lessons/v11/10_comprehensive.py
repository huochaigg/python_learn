"""V11-10 综合练习：闭包、@、*args/**kwargs、返回值、wraps、带参、多层。

学习目标：
1. 自己写一遍从闭包到多层 decorator。
2. 先 TODO，再对照示例答案。
3. 确认装饰发生在定义时，wrapper 发生在调用时。

运行：uv run python lessons/v11/10_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

from functools import wraps


# =============================================================================
# 练习 1
# TODO: 写 make_prefix(prefix)，返回 inner(name)，拼出 "prefix, name"。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


def make_prefix(prefix: str):
    def inner(name: str) -> str:
        return f"{prefix}, {name}"

    return inner


print(make_prefix("Hi")("Ada"))


# =============================================================================
# 练习 2
# TODO: 写 @label，调用前后 print before/after，并用 wraps。
#       装饰 echo(text) -> text，确认返回值不是 None。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


def label(func):
    print(f"[定义阶段] 装饰 {func.__name__}")

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result

    return wrapper


@label
def echo(text: str) -> str:
    """回声。"""
    return text


print("调用 =", echo("hey"))
print("wraps 后 __name__ =", echo.__name__, "__doc__ =", echo.__doc__)


# =============================================================================
# 练习 3
# TODO: 写 @repeat(times)，调用原函数 times 次并返回最后一次结果。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


def repeat(times: int):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(2)
def tick() -> str:
    print("tick")
    return "tock"


print("tick 结果 =", tick())


# =============================================================================
# 练习 4
# TODO: 给 shout 同时加 @label 和 @repeat(2)。
#       想一想等价于 label(repeat(2)(shout)) 还是反过来。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


@label
@repeat(2)
def shout() -> str:
    print("hey")
    return "HEY"


print("多层结果 =", shout())
print("（@label @repeat 等价于 label(repeat(shout))）")

if __name__ == "__main__":
    print("\n--- 10 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 闭包让 inner/wrapper 记住配置和原函数。
# 2. @decorator 等价于 func = decorator(func)。
# 3. wrapper 必须 *args/**kwargs 并 return 原结果。
# 4. 带参 decorator 多一层配置；多个 @ 是嵌套包装。
