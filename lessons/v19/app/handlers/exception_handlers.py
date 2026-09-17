"""异常 → HTTP Response。main 调用 register_exception_handlers(app)。"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from lessons.v19.app.exceptions.base import BizException
from lessons.v19.app.exceptions.business import InsufficientStockError

logger = logging.getLogger("v19")


def _error_body(code: str, message: str, **extra: object) -> dict[str, object]:
    body: dict[str, object] = {"code": code, "message": message, "data": None}
    body.update(extra)
    return body


async def biz_exception_handler(request: Request, exc: BizException) -> JSONResponse:
    # UserNotFoundError 等子类没单独注册时，也会走到这里（按异常 MRO 匹配）。
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(exc.code, exc.message),
    )


async def insufficient_stock_handler(
    request: Request, exc: InsufficientStockError
) -> JSONResponse:
    # 更具体的 handler 优先于 BizException handler，只为观察匹配关系。
    return JSONResponse(
        status_code=exc.status_code,
        content=_error_body(
            exc.code,
            exc.message,
            hint="reduce qty or pick another sku",
        ),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    # RequestValidationError：Path/Query/Body 没通过 FastAPI/Pydantic 校验。
    # 不是业务异常。谁抛的：框架在进 endpoint 之前。
    # HTTP 保持 422，统一的是 JSON 结构，不要为了「统一」改成 200。
    raw = exc.errors()
    # exc.errors()：结构化校验失败列表（loc / type / msg 等）。
    print("[v19] raw RequestValidationError.errors() =", raw)
    slim = [
        {
            "location": [str(part) for part in item.get("loc", ())],
            "message": item.get("msg"),
            "type": item.get("type"),
        }
        for item in raw
    ]
    return JSONResponse(
        status_code=422,
        content={
            "code": "VALIDATION_ERROR",
            "message": "request validation failed",
            "errors": slim,
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # 全局兜底：只处理没被更具体 handler 接住的异常。
    # 客户端只给通用 500，内部细节留在服务端日志。
    # logging.exception(...)：记录当前异常的 traceback，给开发看，不给浏览器。
    logger.exception("unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content=_error_body("INTERNAL_ERROR", "internal server error"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    # app.add_exception_handler(ExcType, func) 等价于 @app.exception_handler(ExcType)
    # 注册「某类异常 → Response」的全局规则。NestJS 对照：ExceptionFilter。
    # 匹配按异常类的 MRO：更具体的类优先。HTTPException 仍走 FastAPI 默认 handler，方便对照。
    #
    # JSONResponse：显式指定 status_code 和 JSON content。
    # 和 endpoint `return dict` 不同：handler 已经离开正常路由返回，必须自己构造 Response。
    # 不要 return Exception 对象本身，也不要带 traceback / 文件路径 / SQL。
    app.add_exception_handler(InsufficientStockError, insufficient_stock_handler)
    app.add_exception_handler(BizException, biz_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
