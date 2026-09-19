"""N+1：循环访问 lazy collection；再用 selectinload 降下来。

运行（项目根目录）：
uv run python -m lessons.v22.n_plus_one_demo
"""

from sqlalchemy import event, select
from sqlalchemy.orm import Session, selectinload

from lessons.v22.app.database import SessionLocal, engine, init_db
from lessons.v22.app.models.order import Order
from lessons.v22.seed import seed


def attach_select_counter() -> dict[str, int]:
    box = {"n": 0}

    def before(conn, cursor, statement, parameters, context, executemany) -> None:
        sql = " ".join(statement.split())
        if not sql.upper().startswith("SELECT"):
            return
        box["n"] += 1
        print(f"  SELECT #{box['n']}: {sql[:180]}")

    event.listen(engine, "before_cursor_execute", before)
    return box


def load_items_lazy(session: Session) -> int:
    # 不加 eager loading：列表 1 条 SQL，每个 order.items 再各 1 条，就是 N+1。
    # N+1 不是 SQLAlchemy 特有，是 ORM 常见问题：关系访问触发隐式 SQL，
    # 列表变大后查询次数跟着涨。官方也提醒 lazy load 很容易变成这样。
    orders = list(session.execute(select(Order).order_by(Order.id)).scalars().all())
    total_items = 0
    for order in orders:
        total_items += len(order.items)
    return total_items


def load_items_selectin(session: Session) -> int:
    # selectinload：eager loading。通常先查父表，再用第二条 SQL
    # WHERE order_id IN (...) 一次加载这些父对象的子集合。
    # 一对多 collection 场景非常实用。
    stmt = select(Order).options(selectinload(Order.items)).order_by(Order.id)
    orders = list(session.execute(stmt).scalars().all())
    return sum(len(order.items) for order in orders)


def main() -> None:
    init_db()
    seed()
    counter = attach_select_counter()

    print("\n===== lazy N+1 (new Session) =====")
    counter["n"] = 0
    session = SessionLocal()
    try:
        n_items = load_items_lazy(session)
        print(f"orders=10, items={n_items}, SELECT count={counter['n']}")
        print("ideal observation: about 11 SELECTs (1 list + 10 item queries).")
        print("exact count can change with cache / extra queries, not a forever guarantee.")
    finally:
        session.close()

    print("\n===== selectinload fix (new Session) =====")
    counter["n"] = 0
    session = SessionLocal()
    try:
        n_items = load_items_selectin(session)
        print(f"orders=10, items={n_items}, SELECT count={counter['n']}")
        print("ideal observation: about 2 SELECTs (orders + items IN (...)).")
    finally:
        session.close()


if __name__ == "__main__":
    main()
    print("\n--- v22 n_plus_one_demo 运行完毕 ---")
