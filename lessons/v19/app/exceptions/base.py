"""业务异常基类。和 V5 的自定义 Exception 是同一思路。"""


class BizException(Exception):
    """承载业务错误语义，不是直接的 HTTP Response。

    Service 只 raise 它（或子类）。FastAPI 的 exception handler 再把它转成 JSON。
    NestJS 对照：throw new BizException(...)，再由 ExceptionFilter 映射 HTTP。
    常见坑：不要把 traceback / SQL / 文件路径塞进 message 给前端。
    """

    def __init__(self, message: str, *, code: str, status_code: int) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        # status_code：这个业务失败对应的 HTTP 状态码，由 handler 写进 Response。
        self.status_code = status_code
