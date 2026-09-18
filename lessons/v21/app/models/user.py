"""User 表。本版加 created_at，方便稳定排序。"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v21.app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    # DateTime：数据库时间列。Python 侧用 datetime 实例读写。
    # default=datetime.now：插入时由 Python 填当前时间。本课不展开 timezone。
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
