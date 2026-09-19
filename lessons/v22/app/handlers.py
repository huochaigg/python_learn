from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lessons.v22.app.exceptions import OrderNotFoundError


async def order_not_found_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": "ORDER_NOT_FOUND", "message": str(exc), "data": None},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(OrderNotFoundError, order_not_found_handler)
