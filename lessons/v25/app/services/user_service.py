"""用户创建。先查 email 只为友好错误；UNIQUE 才是并发兜底。"""

from sqlalchemy import exists, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from lessons.v25.app.exceptions.business import DuplicateEmailError
from lessons.v25.app.models.user import User
from lessons.v25.app.schemas.order import UserCreate


def email_exists(session: Session, email: str) -> bool:
    return bool(session.scalar(select(exists().where(User.email == email))))


class UserService:
    def list_users(self, session: Session) -> list[User]:
        return list(session.execute(select(User).order_by(User.id.asc())).scalars().all())

    def create_user(self, session: Session, data: UserCreate) -> User:
        # 先查：给用户友好错误。这不是并发安全保证。
        # UNIQUE 才是最终防线：两个请求都查到「不存在」时，数据库仍只会放过一个。
        # 先 select 会 autobegin，不要再套 with session.begin()。
        if email_exists(session, data.email):
            raise DuplicateEmailError(data.email)
        user = User(name=data.name, email=data.email)
        session.add(user)
        try:
            session.commit()
        except IntegrityError as extra:
            # IntegrityError：数据库完整性失败信号，不是给前端的文案。
            # 关联 V23：flush/commit 失败后必须 rollback，再转业务异常。
            session.rollback()
            raise DuplicateEmailError(data.email) from extra
        return user
