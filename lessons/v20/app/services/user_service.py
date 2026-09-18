"""用户 CRUD。Router 传入 Session，这里不自己 new 全局 Session。"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from lessons.v20.app.exceptions import EmailTakenError, UserNotFoundError
from lessons.v20.app.models.user import User
from lessons.v20.app.schemas.user import UserCreate, UserUpdate


class UserService:
    def create(self, session: Session, data: UserCreate) -> User:
        user = User(
            name=data.name,
            email=data.email,
            age=data.age,
            nickname=data.nickname,
        )
        # session.add(obj)：把对象纳入当前 Session 的持久化管理。
        # 此刻还没有最终提交；事务里的 INSERT 要等 flush/commit。
        # Prisma 对照：prisma.user.create({ data }) 一次完成；这里是对象 + add + commit。
        session.add(user)
        try:
            # session.commit()：提交当前事务。失败时会话会处于需要 rollback 的状态。
            session.commit()
        except IntegrityError:
            session.rollback()
            raise EmailTakenError(data.email)
        # session.refresh(obj)：再从数据库读一遍最新字段（例如自增 id）。
        # 不是每次 CRUD 都必须 refresh；commit 后想拿到库里的最新值时再用。
        session.refresh(user)
        return user

    def get(self, session: Session, user_id: int) -> User:
        # session.get(Model, pk)：按主键取对象。
        # Prisma 对照：findUnique({ where: { id } })，语义接近，不是完全等价。
        user = session.get(User, user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def list_all(self, session: Session) -> list[User]:
        # select(User)：SQLAlchemy 2.x 推荐的查询表达式，不要用旧式 session.query(User)。
        stmt = select(User)
        # session.execute(stmt)：执行 Statement，得到 Result，还不是 list[User]。
        result = session.execute(stmt)
        # scalars()：抽出每一行里的那个 ORM 实体（select(User) 时就是 User）。
        # .all()：变成 Python list。整条链：select → execute → scalars → all。
        return list(result.scalars().all())

    def get_by_email(self, session: Session, email: str) -> User | None:
        # where(...)：构造 SQL WHERE。email 有 unique，本应最多 1 条。
        stmt = select(User).where(User.email == email)
        # scalar_one_or_none()：0 条 → None；1 条 → 对象；多条 → 异常。
        return session.execute(stmt).scalar_one_or_none()

    def update(self, session: Session, user_id: int, data: UserUpdate) -> User:
        user = self.get(session, user_id)
        changes = data.model_dump(exclude_unset=True)
        for field, value in changes.items():
            # setattr(obj, name, value)：按名字写属性，等价于 user.name = ...
            # Session 追踪这个对象，commit 时把脏字段同步成 UPDATE。
            # Prisma 对照：update({ data: { name } }) 传一份 data；这里改的是对象状态。
            setattr(user, field, value)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise EmailTakenError(data.email or "")
        session.refresh(user)
        return user

    def delete(self, session: Session, user_id: int) -> None:
        user = self.get(session, user_id)
        # session.delete(obj)：标记删除，flush/commit 时才真正执行 DELETE。
        # 调用 delete 的那一行还不等于「库里已经没了」。
        session.delete(user)
        session.commit()
