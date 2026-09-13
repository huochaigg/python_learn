"""业务异常。和 V5 自定义异常是同一套：异常也是 class。

NestJS 对比：throw new BizException(...) → 这里 raise BizException(...)。
后面 FastAPI 会再接到 exception handler，类似 ExceptionFilter。
main 只捕获 BizException 及其子类，不要 except Exception 全吞。
"""


class BizException(Exception):
    """可预期的业务失败基类。上层可统一转成 API Error Response。"""

    def to_response(self) -> dict[str, str]:
        return {"error": type(self).__name__, "message": str(self)}


class UserNotFoundError(BizException):
    """用户不存在。"""


class OrderNotFoundError(BizException):
    """订单不存在。"""


class InsufficientStockError(BizException):
    """库存不足。"""


class InvalidOrderStatusError(BizException):
    """当前状态不允许该操作（例如已取消的订单不能再取消）。"""


class PermissionDeniedError(BizException):
    """角色不够。模拟 @Roles，不是真 JWT。"""
