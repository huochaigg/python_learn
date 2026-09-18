"""最小业务异常 handler。不 import v19。"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lessons.v20.app.exceptions import BizException


async def biz_exception_handler(request: Request, exc: BizException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message, "data": None},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BizException, biz_exception_handler)
