"""V5-05 自定义异常：让业务错误有明确名字。

学习目标：
1. 知道异常本质上也是 class。
2. 会写 BizException 以及更具体的子类。
3. 能把这套思路映射到 NestJS 的 BizException。

运行：uv run python lessons/v5/05_custom_exception.py
"""


class BizException(Exception):
    """业务异常基类。所有可预期的业务失败都继承它。

    自定义 Exception 是什么：一个普通 class，只是继承自 Exception（或其子类）。
    用途：用类型表达「这是哪一种业务失败」，而不是全挤在 ValueError 里。
    JS/TS / NestJS 对比：
      throw new BizException(...)
      raise BizException(...)
    后面 FastAPI 会再把它接到 exception handler，类似 NestJS ExceptionFilter。
    """


class UserNotFoundError(BizException):
    """用户不存在。"""


class InsufficientStockError(BizException):
    """库存不足。"""


users = {1: {"id": 1, "name": "Tom"}}
stock = {"sku-1": 3}


def get_user(user_id: int) -> dict[str, int | str]:
    user = users.get(user_id)
    if user is None:
        raise UserNotFoundError(f"user not found: {user_id}")
    return user


def deduct_stock(sku: str, count: int) -> int:
    left = stock.get(sku, 0)
    if count > left:
        raise InsufficientStockError(f"sku={sku} left={left} need={count}")
    return left - count


print("get_user(1) =", get_user(1))
print("deduct_stock('sku-1', 2) =", deduct_stock("sku-1", 2))

try:
    get_user(9)
except UserNotFoundError as e:
    print("捕获到 UserNotFoundError =", e)
except BizException as e:
    print("其他业务异常 =", e)

try:
    deduct_stock("sku-1", 99)
except InsufficientStockError as e:
    print("捕获到 InsufficientStockError =", e)

# 子类也能被父类捕获：except BizException 可以兜住所有业务异常。
try:
    get_user(9)
except BizException as e:
    print("用基类统一接住 =", type(e).__name__, e)

# 错误示例：用户不存在、库存不足、订单已支付全部 raise ValueError。
# 上层没法区分该回 404 还是 409。
# 正确示例：每种业务失败一个明确类型，上层按类型映射响应。

if __name__ == "__main__":
    print("\n--- 05 自定义异常 运行完毕 ---")

# 本文件重点：
# 1. 异常是 class；自定义异常就是继承 Exception。
# 2. BizException → UserNotFoundError / InsufficientStockError，语义比全用 ValueError 清楚。
# 3. 这和 NestJS 里 throw new BizException 是同一类设计。
# 4. 上层可以先抓子类，再用 BizException 做业务兜底。
