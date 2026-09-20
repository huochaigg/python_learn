"""库存。version_id 给乐观锁教学用；原子 UPDATE 不会自动走这套检查。"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from lessons.v24.app.models.base import Base


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    # version_id：乐观锁版本列，非空整数。不是业务库存字段。
    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # __mapper_args__：给这个 Mapper 的额外配置。
    # version_id_col：开启 ORM Version Counter。flush 时 UPDATE/DELETE 会带上
    # WHERE version_id = :旧版本，成功后再把版本 +1。
    # 用来发现「内存里的对象已经过期 / 别人先改过」。
    # 注意：只作用于针对这个 ORM 对象的 Session.flush() UPDATE/DELETE；
    # 直接 sqlalchemy.update() / bulk DELETE 不会自动获得同一套 version 检查。
    __mapper_args__ = {"version_id_col": version_id}
