from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    # AsyncAttrs：提供 awaitable_attrs 等方式显式访问可能需要异步加载的 ORM 属性。
    # 当前项目主路线仍然优先 selectinload，不要用 AsyncAttrs 掩盖 N+1。
    pass
