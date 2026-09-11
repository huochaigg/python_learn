"""V11-09 后端小场景：日志 / 权限 / 耗时从业务函数里抽出去。

学习目标：
1. 组合 @log_execution、@require_role、@measure_time。
2. 看横切逻辑如何离开 create_order / delete_user。
3. 分清 Decorator 和 Middleware / Interceptor 不是同一个东西。

运行：uv run python lessons/v11/09_backend_scenario.py
"""

from functools import wraps
import time


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[log] call {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[log] done {func.__name__} -> {result}")
        return result

    return wrapper


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        started = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - started) * 1000
        print(f"[time] {func.__name__} {elapsed_ms:.2f}ms")
        return result

    return wrapper


def require_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current = kwargs.get("current_role", "guest")
            if current != role:
                raise PermissionError(f"{func.__name__} needs {role}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@log_execution
@measure_time
@require_role("admin")
def delete_user(user_id: int, current_role: str = "guest") -> str:
    return f"user {user_id} deleted"


@log_execution
@measure_time
def create_order(item: str, current_role: str = "user") -> str:
    time.sleep(0.01)
    return f"order for {item}"


print(create_order("book", current_role="user"))
print(delete_user(7, current_role="admin"))
try:
    delete_user(7, current_role="user")
except PermissionError as e:
    print("拦下 =", e)

# Decorator：贴在单个函数上的横切逻辑（日志、权限、耗时、缓存、重试、事务）。
# Middleware：通常包住整个请求进出，不管具体是哪个 handler。
# Interceptor：更常在调用链前后插入，范围介于两者之间。
# NestJS 里这三套你都见过，不要把 Python @decorator 直接等同于中间件。

if __name__ == "__main__":
    print("\n--- 09 后端场景 运行完毕 ---")

# 本文件重点：
# 1. 业务函数只保留业务，日志/权限/计时用 decorator。
# 2. 多个 @ 仍然是嵌套包装，每层都要 return。
# 3. 权限只是模拟 current_role，没有真 JWT。
# 4. Decorator ≠ Middleware ≠ Interceptor。
