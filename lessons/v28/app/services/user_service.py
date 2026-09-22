from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate


class DuplicateEmailError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(email)


class UserService:
    async def list_users(self, session: AsyncSession) -> list[User]:
        # select/where/order_by 只是构造 Statement，不发生数据库 IO。
        stmt = select(User).order_by(User.id.asc())
        # 真正 execute 才需要 await。Result.scalars().all() 是在已返回 Result 上处理，不额外 await。
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_user(self, session: AsyncSession, user_id: int) -> User | None:
        # session.get 可能访问数据库，因此是 awaitable。
        return await session.get(User, user_id)

    async def create_user(self, session: AsyncSession, data: UserCreate) -> User:
        user = User(name=data.name, email=data.email)
        # add 只改当前 Session 的 ORM 状态，不直接执行网络数据库 IO，所以不 await。
        session.add(user)
        try:
            await session.commit()
        except IntegrityError as extra:
            await session.rollback()
            raise DuplicateEmailError(data.email) from extra
        await session.refresh(user)
        return user

    async def update_user(self, session: AsyncSession, user_id: int, data: UserUpdate) -> User | None:
        user = await session.get(User, user_id)
        if user is None:
            return None
        user.name = data.name
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, session: AsyncSession, user_id: int) -> bool:
        user = await session.get(User, user_id)
        if user is None:
            return False
        await session.delete(user)
        await session.commit()
        return True
