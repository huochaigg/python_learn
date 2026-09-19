"""初始化 SKU 库存。已有数据则跳过。

运行（项目根目录）：
uv run python -m lessons.v23.seed

查看库存：
uv run python -c "from lessons.v23.app.database import SessionLocal, init_db; from lessons.v23.app.models.stock import Stock; from sqlalchemy import select; init_db(); s=SessionLocal(); print([(x.sku, x.quantity) for x in s.execute(select(Stock).order_by(Stock.sku)).scalars()]); s.close()"

或启动后 GET http://127.0.0.1:8001/stocks
"""

from sqlalchemy import func, select

from lessons.v23.app.database import SessionLocal, init_db
from lessons.v23.app.models.stock import Stock

INITIAL = [
    ("A001", 10),
    ("B001", 20),
    ("C001", 5),
]


def seed() -> None:
    init_db()
    session = SessionLocal()
    try:
        existing = session.scalar(select(func.count()).select_from(Stock)) or 0
        if existing > 0:
            print(f"skip seed, stocks already = {existing}")
            for row in session.execute(select(Stock).order_by(Stock.sku)).scalars():
                print(f"  {row.sku} = {row.quantity}")
            return
        for sku, quantity in INITIAL:
            session.add(Stock(sku=sku, quantity=quantity))
        session.commit()
        print("seeded stocks: A001=10, B001=20, C001=5")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
