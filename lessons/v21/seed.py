"""写入 30 个固定测试用户。已有数据则跳过，不会无限插入。

运行（项目根目录）：
uv run python -m lessons.v21.seed
"""

from datetime import datetime, timedelta

from sqlalchemy import func, select

from lessons.v21.app.database import SessionLocal, init_db
from lessons.v21.app.models.user import User

NAMES = [
    "Ada",
    "Tom",
    "Jack",
    "Bob",
    "Eve",
    "Mia",
    "Leo",
    "Amy",
    "Sam",
    "Zoe",
]


def seed() -> None:
    init_db()
    session = SessionLocal()
    try:
        existing = session.scalar(select(func.count()).select_from(User)) or 0
        if existing > 0:
            print(f"skip seed, users already = {existing}")
            return

        rows: list[User] = []
        for i in range(30):
            rows.append(
                User(
                    name=NAMES[i % len(NAMES)] if i < 10 else f"User{i:02d}",
                    email=f"user{i:02d}@example.com",
                    age=18 + (i % 25),
                    active=i % 3 != 0,
                    created_at=datetime(2024, 1, 1) + timedelta(days=i),
                )
            )
        session.add_all(rows)
        session.commit()
        print("seeded 30 users")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
