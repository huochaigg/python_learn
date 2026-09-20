"""订单。只为组合 V23 事务，不展开 Relationship。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lessons.v24.app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_no: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
