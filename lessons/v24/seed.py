"""初始化 SKU。已有数据则跳过。

运行（项目根目录）：
uv run python -m lessons.v24.seed

查看库存：GET http://127.0.0.1:8001/stocks
"""

from sqlalchemy import func, select

from lessons.v24.app.database import SessionLocal, init_db
from lessons.v24.app.models.stock import Stock

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
                print(f"  {row.sku} = {row.quantity} version={row.version_id}")
            return
        for sku, quantity in INITIAL:
            session.add(Stock(sku=sku, quantity=quantity, version_id=1))
        session.commit()
        print("seeded stocks: A001=10, B001=20, C001=5")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
