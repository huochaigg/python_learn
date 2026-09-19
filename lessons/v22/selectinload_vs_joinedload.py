"""selectinload vs joinedload，以及 join() vs joinedload()。

运行（项目根目录）：
uv run python -m lessons.v22.selectinload_vs_joinedload
"""

from sqlalchemy import event, select
from sqlalchemy.orm import joinedload, selectinload

from lessons.v22.app.database import SessionLocal, engine, init_db
from lessons.v22.app.models.order import Order
from lessons.v22.app.models.order_item import OrderItem
from lessons.v22.seed import seed


def attach_select_counter() -> dict[str, int]:
    box = {"n": 0}

    def before(conn, cursor, statement, parameters, context, executemany) -> None:
        sql = " ".join(statement.split())
        if not sql.upper().startswith("SELECT"):
            return
        box["n"] += 1
        print(f"  SELECT #{box['n']}: {sql[:200]}")

    event.listen(engine, "before_cursor_execute", before)
    return box


def main() -> None:
    init_db()
    seed()
    counter = attach_select_counter()

    print("\n===== selectinload: parent query + child IN query =====")
    print("usually two-phase; parent rows are not multiplied by JOIN.")
    counter["n"] = 0
    session = SessionLocal()
    try:
        stmt = select(Order).options(selectinload(Order.items)).order_by(Order.id)
        orders = list(session.execute(stmt).scalars().all())
        print(f"orders={len(orders)} items={sum(len(o.items) for o in orders)} SELECT={counter['n']}")
    finally:
        session.close()

    print("\n===== joinedload: one JOIN query, collection row explosion =====")
    print("not 'one SQL is always faster than two'; pick by cardinality.")
    counter["n"] = 0
    session = SessionLocal()
    try:
        stmt = select(Order).options(joinedload(Order.items)).order_by(Order.id)
        result = session.execute(stmt)
        # unique()：ORM Entity 去重。JOIN 让同一 Order 在结果里出现多次。
        orders = list(result.unique().scalars().all())
        print(f"unique orders={len(orders)} items={sum(len(o.items) for o in orders)} SELECT={counter['n']}")
    finally:
        session.close()

    print("\n===== raw JOIN row count (why unique is needed) =====")
    session = SessionLocal()
    try:
        pair_stmt = select(Order.id, OrderItem.id).join(Order.items).order_by(Order.id, OrderItem.id)
        pairs = list(session.execute(pair_stmt).all())
        order_ids = {row[0] for row in pairs}
        print(f"JOIN rows={len(pairs)} distinct order ids={len(order_ids)}")
        print("collection joinedload has the same row-multiplication shape.")
    finally:
        session.close()

    print("\n===== join() filters query; it is NOT joinedload() =====")
    print("join: change the SQL so we can filter/sort by related table.")
    print("joinedload: load the relationship onto ORM objects.")
    sku = "SKU-APPLE"
    session = SessionLocal()
    try:
        # 可能重复：ORD-000 有两条 SKU-APPLE。
        dup_stmt = select(Order).join(Order.items).where(OrderItem.sku == sku).order_by(Order.id)
        dup_rows = list(session.execute(dup_stmt).scalars().all())
        print(f"join without unique/distinct: {len(dup_rows)} Order objects, ids={[o.id for o in dup_rows]}")

        # unique()：Result/ORM Entity 去重，不是 SQL DISTINCT。
        unique_rows = list(session.execute(dup_stmt).unique().scalars().all())
        print(f"same stmt + Result.unique(): {len(unique_rows)} ids={[o.id for o in unique_rows]}")

        # distinct()：SQL 层生成 DISTINCT。
        distinct_stmt = (
            select(Order)
            .join(Order.items)
            .where(OrderItem.sku == sku)
            .distinct()
            .order_by(Order.id)
        )
        print(distinct_stmt)
        distinct_rows = list(session.execute(distinct_stmt).scalars().all())
        print(f"SQL distinct(): {len(distinct_rows)} ids={[o.id for o in distinct_rows]}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
    print("\n--- v22 selectinload_vs_joinedload 运行完毕 ---")
