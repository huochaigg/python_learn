"""Order：一对多的「一」这一端。items 是 ORM 导航属性，不是 orders 表的列。"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lessons.v22.app.models.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_no: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)

    # relationship()：ORM 对象之间的导航属性，不是数据库列。
    # orders 表里不会真正出现 items 这一列；子行靠 OrderItem.order_id（ForeignKey）关联。
    # ForeignKey 属于数据库列/Schema；relationship 属于 ORM 对象图。
    # SQLAlchemy 常利用 ForeignKey 推导 JOIN 的 ON 条件，但两者不是同一回事。
    #
    # Order.items 是一对多 collection：Mapped[list[OrderItem]]。
    # OrderItem.order 是多对一 scalar：Mapped[Order]。
    # ForeignKey 通常放在「多」的一方，也就是 OrderItem.order_id。
    #
    # back_populates="order"：显式声明两端是同一个双向关系。
    # SQLAlchemy 2.x 官方推荐这种写法，不要把 legacy backref 当主写法。
    #
    # 默认 lazy loading：访问尚未加载的 order.items 时，才会自动再发一条 SELECT。
    # 默认 cascade 是 "save-update, merge"：session.add(order) 时，
    # 集合里还没入库的 OrderItem 也会一起进入 Session。
    # 不要无脑加 cascade="all, delete-orphan"：从 items 移除子对象或删除父订单，
    # 可能直接删掉子行。正式业务必须确认语义，本课保持默认、不配置 delete-orphan。
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem",
        back_populates="order",
    )
