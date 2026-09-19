"""业务异常基类。和 V19 一样：Service raise，handler 转 HTTP。"""


class BizException(Exception):
    def __init__(self, message: str, *, code: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
