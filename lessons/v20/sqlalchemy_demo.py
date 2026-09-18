"""脱离 FastAPI，单独走一遍 SQLAlchemy 生命周期。

重复运行安全：每次用时间戳 email，并在结尾 delete。
flush != commit：flush 后能看到 id，rollback 则库里不会留下那一行。

运行（项目根目录，按模块执行，才能 import lessons.v20）：
uv run python -m lessons.v20.sqlalchemy_demo
"""

from pathlib import Path
from time import time

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from lessons.v20.app.models.base import Base
from lessons.v20.app.models.user import User

DEMO_DB = Path(__file__).resolve().parent / "data" / "demo.db"
DEMO_DB.parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(f"sqlite:///{DEMO_DB}")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)


def main() -> None:
    email = f"demo-{int(time())}@example.com"
    session: Session = SessionLocal()
    try:
        user = User(name="Demo", email=email, age=20)
        session.add(user)
        # flush：把当前变更发到数据库，事务还没最终提交。
        # 这里往往已经能拿到 SQLite 生成的 id。flush != commit。
        session.flush()
        print("after flush id =", user.id, "(transaction not committed)")

        session.commit()
        session.refresh(user)
        print("after commit =", user.id, user.email)

        found = session.get(User, user.id)
        print("get by pk =", found.name if found else None)

        rows = session.execute(select(User).where(User.email == email)).scalars().all()
        print("select where email, count =", len(rows))

        if found:
            found.age = 21
            session.commit()
            session.refresh(found)
            print("updated age =", found.age)

        # 对照：flush 后 rollback，不会留下这行
        ghost = User(name="Ghost", email=f"ghost-{int(time())}@example.com", age=1)
        session.add(ghost)
        session.flush()
        print("ghost flushed id =", ghost.id)
        session.rollback()
        # rollback()：撤销当前事务。flush 过但没 commit 的插入会消失。
        gone = session.execute(select(User).where(User.name == "Ghost")).scalar_one_or_none()
        print("ghost after rollback =", gone)

        still = session.get(User, user.id)
        session.delete(still)
        session.commit()
        print("deleted, get again =", session.get(User, user.id))
    finally:
        session.close()


if __name__ == "__main__":
    main()
    print("--- v20 sqlalchemy_demo 运行完毕 ---")
