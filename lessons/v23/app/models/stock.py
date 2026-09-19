"""库存。本课重点是事务，不展开 Relationship。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v23.app.models.base import Base


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
