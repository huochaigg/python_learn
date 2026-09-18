"""V21 查询表达式 Demo。独立 demo.db，按段 print SQL 和结果。

运行（项目根目录）：
uv run python -m lessons.v21.query_demo
"""

from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import and_, create_engine, exists, func, or_, select
from sqlalchemy.orm import Session, sessionmaker

from lessons.v21.app.models.base import Base
from lessons.v21.app.models.user import User

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEMO_DB = DATA_DIR / "demo.db"

# echo=True：SQLAlchemy 把 SQL 和 bind 参数打到终端。学习方便；
# 生产不要默认一直开，应通过 logging 控制。
engine = create_engine(
    f"sqlite:///{DEMO_DB}",
    echo=True,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine)


def show_sql(title: str, stmt) -> None:
    print(f"\n===== {title} =====")
    # print(stmt) 看到的是 SQL 表达式编译结果；真正执行时参数通常是 bind parameters，
    # 不要自己用 f-string 把用户输入拼进 SQL。
    print(stmt)
    print("--- compiled ---")
    print(stmt.compile(compile_kwargs={"literal_binds": False}))


def seed_demo(session: Session) -> None:
    existing = session.scalar(select(func.count()).select_from(User)) or 0
    if existing > 0:
        print(f"demo db already has {existing} users")
        return
    rows = [
        User(
            name=name,
            email=f"{name.lower()}@example.com",
            age=age,
            active=active,
            created_at=datetime(2024, 1, 1) + timedelta(days=i),
        )
        for i, (name, age, active) in enumerate(
            [
                ("Ada", 20, True),
                ("Tom", 30, True),
                ("Jack", 18, False),
                ("Bob", 25, True),
                ("Eve", 40, False),
                ("Mia", 22, True),
            ]
        )
    ]
    session.add_all(rows)
    session.commit()
    print("seeded 6 demo users")


def names(users: list[User]) -> list[str]:
    return [f"{u.name}(age={u.age},active={u.active})" for u in users]


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed_demo(session)

        # 1) 单 where
        # where()：把 SQL Expression 放进 WHERE。
        # User.age >= 18 不是立刻得到 Python bool，而是生成 SQL 比较表达式。
        stmt = select(User).where(User.age >= 18)
        show_sql("1 single where", stmt)
        print("result:", names(list(session.execute(stmt).scalars().all())))

        # 2) 多个 AND：连续 where，以及 where(a, b) / where(*conditions)
        stmt_chain = select(User).where(User.active.is_(True)).where(User.age >= 20)
        show_sql("2a chained where (AND)", stmt_chain)
        print("result:", names(list(session.execute(stmt_chain).scalars().all())))

        stmt_multi = select(User).where(User.active.is_(True), User.age >= 20)
        show_sql("2b where(a, b) (AND)", stmt_multi)
        conditions = [User.active.is_(True), User.age >= 20]
        stmt_star = select(User).where(*conditions)
        show_sql("2c where(*conditions) (AND)", stmt_star)
        print("result:", names(list(session.execute(stmt_star).scalars().all())))

        # 3) and_() 教学：显式把多个条件组合成 AND。
        # 动态列表很长或要和 OR 嵌套时有用；普通 where(*conditions) 已经够清晰时不必强行用。
        stmt_and = select(User).where(and_(User.active.is_(True), User.age >= 20))
        show_sql("3 and_()", stmt_and)
        print("result:", names(list(session.execute(stmt_and).scalars().all())))

        # 4) or_()：生成 SQL OR，不是 Python or。
        # 错误示范（不要这么写）：
        # User.name.contains("a") or User.email.contains("a")
        stmt_or = select(User).where(
            or_(User.name.contains("a"), User.email.contains("a"))
        )
        show_sql("4 or_()", stmt_or)
        print("result:", names(list(session.execute(stmt_or).scalars().all())))

        # 5) in_()：生成 SQL IN (...)。不要和 Python `value in list` 混淆。
        stmt_in = select(User).where(User.age.in_([18, 20, 22]))
        show_sql("5 in_()", stmt_in)
        print("result:", names(list(session.execute(stmt_in).scalars().all())))

        # 6) contains / like / ilike
        # contains("d") 大致 LIKE '%d%'（包含）。
        # like("A%") 是 SQL LIKE；ilike 是大小写不敏感 LIKE。
        # MySQL / PostgreSQL / SQLite 的大小写行为可能不同，本课不展开 collation。
        stmt_contains = select(User).where(User.name.contains("a"))
        show_sql("6a contains", stmt_contains)
        print("result:", names(list(session.execute(stmt_contains).scalars().all())))
        stmt_like = select(User).where(User.name.like("A%"))
        show_sql("6b like", stmt_like)
        print("result:", names(list(session.execute(stmt_like).scalars().all())))
        stmt_ilike = select(User).where(User.email.ilike("%ADA%"))
        show_sql("6c ilike", stmt_ilike)
        print("result:", names(list(session.execute(stmt_ilike).scalars().all())))

        # 7) order_by / asc / desc
        # order_by 生成 ORDER BY；.asc() / .desc() 对应升序/降序。
        # 分页必须明确排序，否则数据库不承诺稳定顺序。
        stmt_order = select(User).order_by(User.created_at.desc(), User.id.desc())
        show_sql("7 order_by desc", stmt_order)
        print("result:", names(list(session.execute(stmt_order).scalars().all())))

        # 8) limit / offset
        # offset：跳过多少行；limit：最多取多少行。
        # 页码分页：offset = (page - 1) * page_size。
        stmt_page = (
            select(User)
            .order_by(User.id.asc())
            .offset((2 - 1) * 2)
            .limit(2)
        )
        show_sql("8 limit/offset page=2 page_size=2", stmt_page)
        print("result:", names(list(session.execute(stmt_page).scalars().all())))

        # 9) slice(start, stop)：另一种写成 LIMIT/OFFSET 的方式。
        # 主业务分页仍优先显式 offset/limit，更容易对应 page/page_size。
        stmt_slice = select(User).order_by(User.id.asc()).slice(2, 4)
        show_sql("9 slice(2, 4)", stmt_slice)
        print("result:", names(list(session.execute(stmt_slice).scalars().all())))

        # 10) func.count + session.scalar
        # func 用来构造 SQL 函数；COUNT 交给数据库，不要查出全部再 len()。
        # count 复用筛选条件，但不要带 offset/limit。
        count_stmt = (
            select(func.count())
            .select_from(User)
            .where(User.active.is_(True))
        )
        show_sql("10 count", count_stmt)
        # session.scalar：只要第一行第一列单个值，适合 COUNT。
        total = session.scalar(count_stmt)
        print("total active:", total)

        # 11) exists：只关心有没有记录，不加载完整对象。
        exists_stmt = select(exists().where(User.email == "ada@example.com"))
        show_sql("11 exists", exists_stmt)
        print("ada exists:", session.scalar(exists_stmt))
        missing_stmt = select(exists().where(User.email == "nobody@example.com"))
        print("nobody exists:", session.scalar(missing_stmt))

        # 12) 三种查法对照
        print("\n===== 12 get / scalar_one_or_none / exists =====")
        by_pk = session.get(User, 1)
        print("session.get(User, 1):", None if by_pk is None else by_pk.name)
        one = session.execute(
            select(User).where(User.email == "tom@example.com")
        ).scalar_one_or_none()
        print("scalar_one_or_none by email:", None if one is None else one.name)
        print(
            "exists by email:",
            session.scalar(select(exists().where(User.email == "tom@example.com"))),
        )
    finally:
        session.close()


if __name__ == "__main__":
    main()
    print("\n--- v21 query_demo 运行完毕 ---")
