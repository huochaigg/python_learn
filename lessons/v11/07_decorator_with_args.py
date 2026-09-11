"""V11-07 带参数的 decorator：多一层配置函数。

学习目标：
1. 看懂三层：配置层 → decorator 层 → wrapper 层。
2. 知道 @repeat(3) 会先执行 repeat(3)，得到真正的 decorator。
3. 再用 require_role 看后端权限这种形态。

运行：uv run python lessons/v11/07_decorator_with_args.py
"""

from functools import wraps


def repeat(times: int):
    # 第 1 层 配置层：接收 decorator 自己的参数。@repeat(3) 会先调用这里。
    def decorator(func):
        # 第 2 层 decorator 层：接收被装饰的函数。
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 第 3 层 wrapper 层：接收业务调用时的参数。
            result = None
            for i in range(times):
                print(f"  repeat #{i + 1}")
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def ping() -> str:
    print("ping")
    return "pong"


print("[定义阶段] @repeat(3) 已经应用完")
print("[调用阶段] 开始 ping()")
print("结果 =", ping())


def require_role(role: str):
    # 概念上类似 NestJS 的 @Roles("admin")：声明时带配置，调用时再检查。
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current = kwargs.get("current_role", "guest")
            if current != role:
                raise PermissionError(f"need {role}, got {current}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@require_role("admin")
def delete_user(user_id: int, current_role: str = "guest") -> str:
    return f"deleted {user_id}"


print("\n管理员删除 =", delete_user(1, current_role="admin"))
try:
    delete_user(1, current_role="user")
except PermissionError as e:
    print("权限不足 =", e)

if __name__ == "__main__":
    print("\n--- 07 带参数 decorator 运行完毕 ---")

# 本文件重点：
# 1. @repeat(3) = 先 repeat(3) 得到 decorator，再 decorator(func)。
# 2. 三层分别是：配置、接收 func、接收调用参数。
# 3. 配置靠闭包传进 wrapper。
# 4. @Roles("admin") 是同一类「带参数的声明」，实现栈不同。
