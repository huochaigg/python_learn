"""User ORM Model ↔ 数据库 users 表。实例 ↔ 某一行。"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v20.app.models.base import Base


class User(Base):
    __tablename__ = "users"

    # Mapped[int]：这是 ORM 映射属性，不是普通 Python 字段。
    # 同时给 IDE/类型检查器用。Prisma 对照：model User { id Int @id }
    #
    # mapped_column()：列的 ORM/数据库配置（主键、唯一、索引、可空、默认值等）。
    # SQLAlchemy 2.x 会结合 Mapped[...] 推导类型和一部分 nullability。
    # 关键字段本课仍显式写 nullable，方便对照表结构。
    #
    # primary_key=True：这一列是主键。SQLite 整型主键通常会自动递增。
    id: Mapped[int] = mapped_column(primary_key=True)

    # nullable=False：数据库不允许 NULL。Mapped[str] 通常也表示不能是 None。
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    # unique=True：email 不能重复。index=True：给查询建索引。
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    age: Mapped[int] = mapped_column(nullable=False)

    # default=True：插入时如果没给值，ORM/数据库侧用这个默认。
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Mapped[str | None]：属性允许 None；通常对应可空列。
    # Mapped[str] 则偏向非空。2.x 能从 annotation 推导一部分 nullability，
    # 这里仍写 nullable=True，方便第一轮把「类型」和「列」对上。
    nickname: Mapped[str | None] = mapped_column(String(50), nullable=True)
