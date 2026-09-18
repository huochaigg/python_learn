from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from lessons.v21.app.exceptions import UserNotFoundError


async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"code": "USER_NOT_FOUND", "message": str(exc), "data": None},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UserNotFoundError, user_not_found_handler)
