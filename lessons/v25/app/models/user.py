"""User。email 的 UNIQUE 是数据库最终防线。"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v25.app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    # nullable=False：数据库 NOT NULL。Pydantic required 是请求层；这里是库表层。
    # 两层都要有。应用漏校验时，数据库仍会拒绝 NULL。
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # unique=True：数据库层要求该列值唯一。
    # 即使应用层漏掉 email_exists、两个请求同时插入，数据库仍会拒绝重复值。
    # 先查只改善体验，UNIQUE 才是并发最终兜底。
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
