"""共享依赖：分页、Class Dependency、Request 级 cache Demo。"""

from typing import Annotated

from fastapi import Depends, Query

from lessons.v18.app.schemas.common import PaginationParams

# Depends(callable)：声明「当前参数/依赖需要这个 callable 在本次 HTTP 请求里跑出来的结果」。
# 传入的是函数本身 Depends(get_pagination)，不是 Depends(get_pagination())。
# 错误写法 Depends(get_pagination()) 会在 Python 执行到这一行时立刻调用函数，
# 把返回值交给 Depends；FastAPI 拿到的就不是 callable，依赖图也建不起来。
# 真正调用发生在「处理这一次 Request」时，不是应用启动时跑一次，也不是全局单例。
#
# NestJS 对照：目的都是注入依赖。Nest 更常 constructor + Provider/IoC 容器里的长期 Service；
# FastAPI 更常 endpoint 参数上声明 request-driven 依赖图，每次请求现算。
# Depends 默认 cache 也只是「同一 Request 内复用」，不是 Nest Singleton，不是 Redis。


def get_pagination(
    page: Annotated[int, Query(ge=1, description="页码，从 1 开始")] = 1,
    limit: Annotated[int, Query(ge=1, le=100, description="每页条数")] = 20,
    keyword: Annotated[str | None, Query(max_length=50)] = None,
) -> PaginationParams:
    # Dependency 自己也可以声明 Query/Path/Header。FastAPI 会一起解析，并写进 OpenAPI。
    # 所以 users、orders 都能复用同一套分页参数，Swagger 里也会看到 page/limit/keyword。
    return PaginationParams(page=page, limit=limit, keyword=keyword)


# Annotated[PaginationParams, Depends(get_pagination)]：
# - 前面的 PaginationParams：告诉 IDE/类型检查器，endpoint 里这个参数是什么类型。
# - Depends(get_pagination)：metadata，告诉 FastAPI 这个值从哪个 callable 来。
# 官方当前推荐这种写法。老项目还可能看到：
#   pagination: PaginationParams = Depends(get_pagination)
# 本课主代码用 Annotated。
PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]


class CommonQueryParams:
    """Class Dependency：class 本身是 callable，FastAPI 会调用它来 new 实例再注入。

    官方也支持 Annotated[CommonQueryParams, Depends()] 这种简写（缺省就是这个 class）。
    主学习代码写成 Depends(CommonQueryParams)，更容易看出「注入的是谁」。
    """

    def __init__(
        self,
        keyword: Annotated[str | None, Query()] = None,
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
    ) -> None:
        self.keyword = keyword
        self.skip = skip
        self.limit = limit


_marker_calls = 0


def get_request_marker() -> str:
    # 每次「真正执行」才 +1。同一次 Request 里默认 use_cache=True，通常只跑一次。
    # 这是单 Request 结果复用，进程一关、下一个请求、换一台机器都不会接着用。
    global _marker_calls
    _marker_calls += 1
    marker = f"m{_marker_calls}"
    print(f"[dep] get_request_marker run #{_marker_calls} -> {marker}")
    return marker
