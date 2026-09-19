"""写入 10 个订单，每个 2～5 条明细。已有数据则跳过。

运行（项目根目录）：
uv run python -m lessons.v22.seed
"""

from sqlalchemy import func, select

from lessons.v22.app.database import SessionLocal, init_db
from lessons.v22.app.models.order import Order
from lessons.v22.app.models.order_item import OrderItem

STATUSES = ["pending", "paid", "shipped"]
PRODUCTS = [
    ("SKU-APPLE", "Apple", 5),
    ("SKU-BANANA", "Banana", 3),
    ("SKU-MILK", "Milk", 8),
    ("SKU-BREAD", "Bread", 4),
    ("SKU-EGG", "Egg", 2),
]


def seed() -> None:
    init_db()
    session = SessionLocal()
    try:
        existing = session.scalar(select(func.count()).select_from(Order)) or 0
        if existing > 0:
            print(f"skip seed, orders already = {existing}")
            return

        for i in range(10):
            order = Order(order_no=f"ORD-{i:03d}", status=STATUSES[i % 3])
            n_items = 2 + (i % 4)
            for j in range(n_items):
                sku, name, price = PRODUCTS[(i + j) % len(PRODUCTS)]
                order.items.append(
                    OrderItem(sku=sku, name=name, price=price, quantity=1 + j)
                )
            if i == 0:
                # 同一订单两条 SKU-APPLE，方便观察 join 后父对象重复。
                order.items.append(
                    OrderItem(sku="SKU-APPLE", name="Apple Bag", price=12, quantity=1)
                )
            session.add(order)

        session.commit()
        item_count = session.scalar(select(func.count()).select_from(OrderItem)) or 0
        print(f"seeded 10 orders, {item_count} items")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
