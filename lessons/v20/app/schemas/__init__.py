"""Schema 包。SQLAlchemy Model 管表；这里只管 HTTP 输入输出。"""

from lessons.v20.app.schemas.user import UserCreate, UserResponse, UserUpdate

__all__ = ["UserCreate", "UserResponse", "UserUpdate"]
