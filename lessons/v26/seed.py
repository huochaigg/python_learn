"""
文件作用：初始化 V26 演示数据库
运行命令：uv run python lessons/v26/seed.py
重点概念：create_all 前 import Model；固定测试账户；可重复 seed。
观察重点：数据库是否创建表，并插入固定测试数据
"""

from sqlalchemy import func, inspect, select

from app.database import DB_PATH, SessionLocal, engine, init_db
from app.models.account import Account

INITIAL = [
    ("A", 100),
    ("B", 200),
    ("C", 50),
]


def seed() -> None:
    init_db()
    session = SessionLocal()
    try:
        existing = int(session.scalar(select(func.count()).select_from(Account)) or 0)
        if existing == 0:
            for name, balance in INITIAL:
                session.add(Account(name=name, balance=balance))
            session.commit()
            print("inserted", len(INITIAL), "accounts")
        else:
            print("skip insert, accounts already =", existing)

        rows = list(session.execute(select(Account).order_by(Account.name)).scalars())
        print("db =", DB_PATH)
        print("tables =", inspect(engine).get_table_names())
        print("count =", len(rows))
        for row in rows:
            print(f"  {row.name} balance={row.balance}")
        assert len(rows) >= 2
    finally:
        session.close()


if __name__ == "__main__":
    seed()
    print("--- v26 seed 运行完毕 ---")
