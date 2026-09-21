from lessons.v25.app.exceptions.base import BizException


class DuplicateEmailError(BizException):
    def __init__(self, email: str) -> None:
        super().__init__(
            f"email already taken: {email}",
            code="DUPLICATE_EMAIL",
            status_code=409,
        )
        self.email = email


class DuplicateRequestError(BizException):
    def __init__(self, idempotency_key: str) -> None:
        super().__init__(
            f"duplicate request already processed: {idempotency_key}",
            code="DUPLICATE_REQUEST",
            status_code=409,
        )
        self.idempotency_key = idempotency_key


class DataIntegrityError(BizException):
    def __init__(self, message: str = "data integrity conflict") -> None:
        super().__init__(message, code="DATA_INTEGRITY", status_code=409)


class OrderNotFoundError(BizException):
    def __init__(self, ident: str) -> None:
        super().__init__(
            f"order not found: {ident}",
            code="ORDER_NOT_FOUND",
            status_code=404,
        )
