"""Account：V26 最小演示表，只用来证明 SQLite 里有真实数据。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
