"""Depends 教学接口：class / yield / cache / router-level check。"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from lessons.v18.app.dependencies.auth import verify_request_header
from lessons.v18.app.dependencies.common import CommonQueryParams, get_request_marker
from lessons.v18.app.dependencies.resources import (
    FakeDatabaseSession,
    get_async_client,
    get_session,
)

router = APIRouter(prefix="/demo", tags=["depends-demo"])

# Router-level dependencies：列表里的 Depends 每次请求都会跑，但返回值不会注入函数参数。
# 适合「必须检查，endpoint 不需要那个对象」——有点像 Nest Guard 的一部分用途，不是等价物。
need_client = APIRouter(dependencies=[Depends(verify_request_header)])


@need_client.get("/need-client")
def need_client_ok() -> dict[str, str]:
    return {"ok": "header checked, endpoint got no return value from it"}


router.include_router(need_client)


@router.get("/query")
def class_query(
    query: Annotated[CommonQueryParams, Depends(CommonQueryParams)],
) -> dict[str, Any]:
    # Class Dependency：FastAPI 调用 CommonQueryParams(...) 得到实例。
    # endpoint 直接用 query.keyword / query.limit。
    # 简写也可以：Annotated[CommonQueryParams, Depends()]，本课保留显式 class 名。
    return {"keyword": query.keyword, "skip": query.skip, "limit": query.limit}


@router.get("/session")
def use_session(
    session: Annotated[FakeDatabaseSession, Depends(get_session)],
) -> dict[str, Any]:
    return {"rows": session.query_users()}


@router.get("/session-error")
def session_error(
    session: Annotated[FakeDatabaseSession, Depends(get_session)],
) -> dict[str, Any]:
    # 主动抛错：终端仍应看到 session close。清理不能依赖 endpoint 正常 return。
    session.query_users()
    raise RuntimeError("boom after query")


@router.get("/async-client")
async def use_async_client(
    client: Annotated[dict[str, str], Depends(get_async_client)],
) -> dict[str, str]:
    return {"client": client["name"]}


def _use_marker(marker: Annotated[str, Depends(get_request_marker)]) -> str:
    return marker


@router.get("/cache-on")
def cache_on(
    a: Annotated[str, Depends(_use_marker)],
    b: Annotated[str, Depends(_use_marker)],
    marker: Annotated[str, Depends(get_request_marker)],
) -> dict[str, str]:
    # 默认同一次 Request 里 get_request_marker 只执行一次，a/b/marker 相同。
    # Depends(..., use_cache=True) 是默认值：单 Request 复用，不是 Redis。
    return {"a": a, "b": b, "marker": marker}


@router.get("/cache-off")
def cache_off(
    first: Annotated[str, Depends(get_request_marker, use_cache=False)],
    second: Annotated[str, Depends(get_request_marker, use_cache=False)],
) -> dict[str, str]:
    # use_cache=False：同一请求也会重新执行。只为理解，业务代码别到处关。
    return {"first": first, "second": second}


@router.get("/header-check", dependencies=[Depends(verify_request_header)])
def path_level_check() -> dict[str, str]:
    # path-level dependencies=[...]：和 Router-level 同一机制，作用范围只是这一条。
    return {"ok": "path-level header check"}
