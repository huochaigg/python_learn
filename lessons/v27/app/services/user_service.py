from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models.user import User
from ..schemas.user import UserCreate


class DuplicateEmailError(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(email)


class UserService:
    def list_users(self, session: Session) -> list[User]:
        return list(session.execute(select(User).order_by(User.id.asc())).scalars().all())

    def get_user(self, session: Session, user_id: int) -> User | None:
        return session.get(User, user_id)

    def create_user(self, session: Session, data: UserCreate) -> User:
        user = User(name=data.name, email=data.email)
        session.add(user)
        try:
            session.commit()
        except IntegrityError as extra:
            session.rollback()
            raise DuplicateEmailError(data.email) from extra
        session.refresh(user)
        return user
