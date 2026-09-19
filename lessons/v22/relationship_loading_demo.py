"""三种加载策略对比。每段换新 Session，避免 Identity Map 干扰。

运行（项目根目录）：
uv run python -m lessons.v22.relationship_loading_demo
"""

from sqlalchemy import event, select
from sqlalchemy.orm import Session, joinedload, selectinload

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


def with_new_session(title: str, counter: dict[str, int], fn) -> None:
    print(f"\n===== {title} =====")
    counter["n"] = 0
    # 同一 Session 会缓存/跟踪已加载 ORM 实例（Identity Map），
    # 关系一旦加载过，再访问可能不再发 SQL。教学对比用独立 Session。细节后续再讲。
    session = SessionLocal()
    try:
        fn(session)
        print(f"SELECT count={counter['n']}")
    finally:
        session.close()


def demo_lazy(session: Session) -> None:
    order = session.get(Order, 1)
    print("order", order.order_no)
    print("items", [item.sku for item in order.items])


def demo_selectin(session: Session) -> None:
    stmt = select(Order).where(Order.id == 1).options(selectinload(Order.items))
    order = session.execute(stmt).scalar_one()
    print("order", order.order_no)
    print("items", [item.sku for item in order.items])


def demo_joined(session: Session) -> None:
    # joinedload：通过 JOIN 把 relationship 一起取回，也是 eager loading。
    # 对 collection 使用时，父表行会因多个子记录在 SQL Result 中重复（行乘法）。
    stmt = select(Order).where(Order.id == 1).options(joinedload(Order.items))
    # unique()：JOIN 结果里一个 Order 可能对应多行，让 Result 对 ORM Entity 唯一化。
    # 它不是 SQL DISTINCT。
    order = session.execute(stmt).unique().scalar_one()
    print("order", order.order_no)
    print("items", [item.sku for item in order.items])


def main() -> None:
    init_db()
    seed()
    counter = attach_select_counter()
    with_new_session("lazy: get Order then access items", counter, demo_lazy)
    with_new_session("selectinload(Order.items)", counter, demo_selectin)
    with_new_session("joinedload(Order.items) + unique()", counter, demo_joined)


if __name__ == "__main__":
    main()
    print("\n--- v22 relationship_loading_demo 运行完毕 ---")
