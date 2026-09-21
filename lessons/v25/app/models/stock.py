"""库存。CHECK 约束保证 quantity >= 0。"""

from sqlalchemy import CheckConstraint, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v25.app.models.base import Base


class Stock(Base):
    __tablename__ = "stocks"
    # CheckConstraint：数据库检查逻辑表达式，违反则拒绝写入。
    # name=...：给约束命名，方便 Migration、日志定位、按名字转业务错误。
    # 本课不展开各库 CHECK 实现差异。
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="ck_stock_quantity_non_negative"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
