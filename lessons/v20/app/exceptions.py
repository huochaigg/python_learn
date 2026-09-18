"""V20 小型业务异常。不 import lessons.v19，版本独立可跑。"""


class BizException(Exception):
    def __init__(self, message: str, *, code: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class UserNotFoundError(BizException):
    def __init__(self, user_id: int) -> None:
        super().__init__(
            f"user not found: {user_id}",
            code="USER_NOT_FOUND",
            status_code=404,
        )


class EmailTakenError(BizException):
    def __init__(self, email: str) -> None:
        super().__init__(
            f"email already taken: {email}",
            code="EMAIL_TAKEN",
            status_code=409,
        )
