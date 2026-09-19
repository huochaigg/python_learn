"""OrderItem：一对多的「多」这一端。ForeignKey 放在这里。"""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lessons.v22.app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    # ForeignKey("orders.id")：数据库列/Schema 层约束，表示本列引用 orders 表主键。
    # 它不等于 ORM relationship：表里真正存在的是 order_id 这一列。
    # SQLAlchemy 可以利用它推导 relationship 的 JOIN 条件（ON order_items.order_id = orders.id）。
    # ForeignKey 通常放在「多」的一方（many-to-one 这边）。
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False, index=True)
    sku: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # 多对一：item.order 是单个 Order，不是 list。
    # back_populates="items" 与 Order.items 成对，表示同一个双向关系。
    order: Mapped["Order"] = relationship("Order", back_populates="items")
