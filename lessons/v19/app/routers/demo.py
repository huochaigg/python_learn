"""教学接口：HTTPException / 校验失败 / 未知异常。正式项目不会故意留 unexpected-error。"""

from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Path, Query, status

router = APIRouter(prefix="/demo", tags=["exception-demo"])


@router.get("/http-exception/{item_id}")
def http_exception_demo(item_id: int) -> dict[str, int]:
    # HTTPException：HTTP 层错误。status_code = HTTP 状态码，detail = 默认错误内容。
    # raise 会立刻中断正常流程，交给 FastAPI 已有的 HTTPException handler。
    # NestJS 对照：throw new HttpException / NotFoundException。
    #
    # 和 return {"error": "..."} 的区别：
    # return dict 仍是普通 200 JSON，除非你自己改 Response；
    # raise HTTPException 才进入异常流程。不要用 return 模拟失败。
    #
    # 和 BizException 的区别：HTTPException 绑在 FastAPI/HTTP 上；
    # Service 更适合 raise 业务异常，由 handler 做 HTTP mapping。
    if item_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="item not found",
        )
    return {"id": item_id}


@router.get("/http-exception-headers")
def http_exception_headers(
    authorization: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    # headers=...：额外的 HTTP Response Headers。这里只模拟认证失败，不是真 JWT/OAuth2。
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
            headers={
                "WWW-Authenticate": "Bearer",
                "X-Demo-Reason": "missing-token",
            },
        )
    return {"ok": "header present (still fake auth)"}


@router.get("/validation/{item_id}")
def validation_demo(
    item_id: Annotated[int, Path(ge=1)],
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> dict[str, int]:
    # 故意传 /demo/validation/abc 或 ?limit=0，观察 RequestValidationError handler → 422。
    return {"item_id": item_id, "limit": limit}


@router.get("/unexpected-error")
def unexpected_error() -> dict[str, str]:
    # 教学用：故意 RuntimeError，看全局 Exception handler 返回 500 通用信息。
    # 正式项目不要保留这种接口。
    raise RuntimeError("do not leak this message to the client")
