"""横切逻辑：日志、计时、权限。复习 V11 decorator。"""

import inspect
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from lessons.v15.order_app.exceptions import PermissionDeniedError


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """记录调用开始/结束。同步、异步各走一条 wrapper。

    inspect.iscoroutinefunction(func)：判断是不是 coroutine function（async def + 通常 return）。
    用途：决定要不要 await。Async Generator（async def + yield）这里不要拿来装饰。
    和 V11 同步 decorator 的区别：async 版本的 wrapper 自己也必须是 async def，内部 await 原函数。
    """
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            print(f"  [log] start {func.__name__}")
            result = await func(*args, **kwargs)
            print(f"  [log] end   {func.__name__}")
            return result

        return async_wrapper

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"  [log] start {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [log] end   {func.__name__}")
        return result

    return wrapper


def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """异步计时 decorator。只包 async def，保持实现简单。"""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        started = time.perf_counter()
        result = await func(*args, **kwargs)
        cost = time.perf_counter() - started
        print(f"  [time] {func.__name__} {cost:.3f}s")
        return result

    return wrapper


def require_role(role: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """带参数 decorator 三层结构：配置层 -> decorator 层 -> wrapper 层。

    @require_role("admin") 先调用 require_role("admin") 得到真正的 decorator。
    角色通过调用时的 current_role=... 传入，不做 JWT。
    NestJS 对比：概念接近 @Roles("admin")，实现栈完全不同。
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current = kwargs.get("current_role", "guest")
            if current != role:
                raise PermissionDeniedError(f"need {role}, got {current}")
            return await func(*args, **kwargs)

        return wrapper

    return decorator
