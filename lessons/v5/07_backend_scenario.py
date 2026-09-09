"""V5-07 后端小场景：下单扣库存。

学习目标：
1. 用「正常流程 return，异常流程 raise」写一层 service。
2. 参数非法、订单不存在、库存不足分别用不同异常。
3. 最外层按异常类型打印模拟 HTTP 响应。

运行：uv run python lessons/v5/07_backend_scenario.py
"""


class BizException(Exception):
    """可预期的业务失败。"""


class OrderNotFoundError(BizException):
    """订单不存在。"""


class InsufficientStockError(BizException):
    """库存不足。"""


ORDERS: dict[str, dict[str, int | str]] = {
    "o1": {"id": "o1", "sku": "book", "stock": 5},
}


def place_order(order_id: str, buy_count: int) -> dict[str, int | str]:
    """下单：校验 → 找订单 → 扣库存语义（这里只计算剩余，方便反复跑）。

    正常：return 结果。
    异常：raise，不返回 None / {"ok": False}。
    """
    if buy_count <= 0:
        raise ValueError("buy_count must be > 0")

    order = ORDERS.get(order_id)
    if order is None:
        raise OrderNotFoundError(f"order not found: {order_id}")

    stock = int(order["stock"])
    if buy_count > stock:
        raise InsufficientStockError(
            f"order={order_id} stock={stock} need={buy_count}"
        )

    return {
        "order_id": order_id,
        "sku": str(order["sku"]),
        "bought": buy_count,
        "remaining": stock - buy_count,
    }


def handle(order_id: str, buy_count: int) -> None:
    """模拟路由层：把异常映射成响应，而不是让进程崩掉。"""
    try:
        result = place_order(order_id, buy_count)
    except OrderNotFoundError as e:
        print("  -> 404", e)
    except InsufficientStockError as e:
        print("  -> 409", e)
    except ValueError as e:
        print("  -> 400", e)
    except BizException as e:
        print("  -> 400 business", e)
    else:
        print("  -> 200", result)


print("成功下单")
handle("o1", 2)

print("数量非法")
handle("o1", 0)

print("订单不存在")
handle("missing", 1)

print("库存不足")
handle("o1", 99)

if __name__ == "__main__":
    print("\n--- 07 后端场景 运行完毕 ---")

# 本文件重点：
# 1. service：能做完就 return，做不完就 raise。
# 2. ValueError 管入参；OrderNotFoundError / InsufficientStockError 管业务。
# 3. 最外层按类型映射 400 / 404 / 409，类似 NestJS filter / FastAPI handler。
# 4. 不要用一个 ValueError 表达所有失败。
