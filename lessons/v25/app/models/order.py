"""订单。idempotency_key UNIQUE 防止同一请求重复下单。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lessons.v25.app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_no: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    # 幂等 Key：同一个业务请求携带同一个唯一 key。
    # 客户端重试时应复用这个 key，服务端识别后避免重复副作用（不要创建第二份订单）。
    # 幂等不是禁止同一用户下多单；不同 key 可以创建多个订单。
    # 先查 key 是否存在仍有并发窗口，所以 UNIQUE 必须保留。
    idempotency_key: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
