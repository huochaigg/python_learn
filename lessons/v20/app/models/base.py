"""ORM Declarative Base。"""

from sqlalchemy.orm import DeclarativeBase


# DeclarativeBase：SQLAlchemy 2.x 推荐的 ORM 声明式基类。
# 所有 Model 继承它以后，进入同一套 mapping / metadata 系统。
# 旧教程常见 declarative_base() 工厂函数；新项目不要当主写法。
# Prisma 对照：没有完全对等物，更接近「所有 Prisma Model 共用的 schema 注册入口」。
class Base(DeclarativeBase):
    pass
