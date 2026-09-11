"""V11-08 多个 decorator：@A @B 等价于 A(B(func))。

学习目标：
1. 用打印验证包装顺序。
2. 记住：靠近函数的先包进去。
3. 调用时从最外层 wrapper 走进去。

运行：uv run python lessons/v11/08_multiple_decorators.py
"""

from functools import wraps


def A(func):
    print("[定义阶段] 应用 A")

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("进入 A")
        result = func(*args, **kwargs)
        print("退出 A")
        return result

    return wrapper


def B(func):
    print("[定义阶段] 应用 B")

    @wraps(func)
    def wrapper(*args, **kwargs):
        print("进入 B")
        result = func(*args, **kwargs)
        print("退出 B")
        return result

    return wrapper


print("即将定义 demo，装饰器从下往上应用：先 B 再 A")


@A
@B
def demo() -> str:
    print("函数体")
    return "ok"


# 简化等价：demo = A(B(demo))
print("定义结束")
print("调用结果 =", demo())

if __name__ == "__main__":
    print("\n--- 08 多个 decorator 运行完毕 ---")

# 本文件重点：
# 1. @A @B 写在函数上，等价于 A(B(func))。
# 2. 定义阶段通常先执行更靠近函数的 B，再执行 A。
# 3. 调用阶段先进入外层 A，再进入 B，再进函数体，再反向退出。
# 4. 用 print 就能核对嵌套关系，不必背口诀。
