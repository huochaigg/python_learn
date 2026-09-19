"""双向 relationship 怎么建起来；以及 Lazy Loading / many-to-one。

运行（项目根目录）：
uv run python -m lessons.v22.relationship_demo
"""

from pathlib import Path

from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import Session, sessionmaker

from lessons.v22.app.models.base import Base
from lessons.v22.app.models.order import Order
from lessons.v22.app.models.order_item import OrderItem

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DB = DATA_DIR / "relationship_demo.db"

# echo=True：把 SQL 打到终端。只给教学 Demo 用，不要当 FastAPI 默认。
engine = create_engine(
    f"sqlite:///{DEMO_DB}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


@event.listens_for(engine, "connect")
def _fk(dbapi_connection, connection_record) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def show_graph(title: str, order: Order, items: list[OrderItem]) -> None:
    print(f"\n===== {title} =====")
    print("order.items ids/skus:", [(item.id, item.sku) for item in order.items])
    for item in items:
        parent = item.order
        print(
            f"item sku={item.sku} -> item.order is order? {parent is order}",
            f"order_no={None if parent is None else parent.order_no}",
        )


def demo_link_in_memory() -> None:
    order = Order(order_no="DEMO-001", status="pending")
    item_a = OrderItem(sku="SKU-A", name="Alpha", price=10, quantity=1)
    item_b = OrderItem(sku="SKU-B", name="Beta", price=20, quantity=2)

    print("\n===== before linking =====")
    print("order.items =", list(order.items))
    print("item_a.order =", item_a.order)

    # 方式 1：从「多」这一端赋值。back_populates 会把 item_a 同步进 order.items。
    item_a.order = order
    show_graph("after item_a.order = order", order, [item_a, item_b])

    # 方式 2：从「一」这一端 append。back_populates 会把 item_b.order 指回这个 order。
    order.items.append(item_b)
    show_graph("after order.items.append(item_b)", order, [item_a, item_b])

    session = SessionLocal()
    try:
        session.add(order)
        session.commit()
        print("committed order id =", order.id, "item ids =", [item_a.id, item_b.id])
    finally:
        session.close()


def demo_lazy_loading() -> None:
    print("\n===== Lazy Loading =====")
    # Lazy Loading：访问尚未加载的 relationship 时，SQLAlchemy 自动补一条 SELECT。
    # 默认 relationship 常用这种策略。先查 Order 是 1 条 SQL；第一次读 order.items 再发 1 条。
    session = SessionLocal()
    try:
        order = session.get(Order, 1)
        print("got order", None if order is None else order.order_no)
        print("--- access order.items, extra SELECT expected ---")
        items = list(order.items)
        print("items:", [(item.sku, item.quantity) for item in items])
    finally:
        session.close()


def demo_many_to_one() -> None:
    print("\n===== many-to-one item.order =====")
    # 多对一也是 relationship，只是属性是单个对象，不是 list。
    session = SessionLocal()
    try:
        item = session.execute(select(OrderItem).limit(1)).scalar_one()
        print("item", item.sku, "order_id", item.order_id)
        print("--- access item.order, extra SELECT expected ---")
        print("item.order.order_no =", item.order.order_no)
    finally:
        session.close()


def main() -> None:
    DEMO_DB.unlink(missing_ok=True)
    Base.metadata.create_all(bind=engine)
    demo_link_in_memory()
    demo_lazy_loading()
    demo_many_to_one()


if __name__ == "__main__":
    main()
    print("\n--- v22 relationship_demo 运行完毕 ---")
