"""动态 where / 排序 / 分页 / count / exists。逻辑不进 Router。"""

from sqlalchemy import ColumnElement, exists, func, or_, select
from sqlalchemy.orm import Session

from lessons.v21.app.exceptions import UserNotFoundError
from lessons.v21.app.models.user import User
from lessons.v21.app.schemas.user import UserPageResponse, UserQuery, UserResponse

# 排序白名单：前端只能选这些 key，映射到 ORM 列。
# 既限制 API Contract，也避免把用户字符串拼进 SQL。
SORT_COLUMNS = {
    "id": User.id,
    "name": User.name,
    "age": User.age,
    "created_at": User.created_at,
}


def build_conditions(query: UserQuery) -> list[ColumnElement[bool]]:
    # 动态条件用列表收集，最后 where(*conditions)。
    # 不要为每个参数组合写大量 if/else 分支。
    conditions: list[ColumnElement[bool]] = []

    if query.keyword:
        keyword = query.keyword
        # or_()：生成 SQL OR（name LIKE ... OR email LIKE ...）。
        # 不要写 User.name.contains(k) or User.email.contains(k)：
        # 那是 Python or，左右都是 SQL Expression（真值），不会得到你以为的 SQL OR。
        # contains(keyword)：大致对应 SQL LIKE '%keyword%'（包含匹配）。
        conditions.append(
            or_(User.name.contains(keyword), User.email.contains(keyword))
        )

    # 必须用 `is not None`。`if query.active:` 会把 False 当成「没筛选」，
    # 于是 active=false 查不到「停用用户」，条件被悄悄丢掉。
    if query.active is not None:
        conditions.append(User.active == query.active)

    if query.min_age is not None:
        # User.age >= 18 是 SQL Expression，不是立刻算出来的 Python bool。
        # where() 把这些 Expression 放进 SQL WHERE。
        conditions.append(User.age >= query.min_age)

    if query.max_age is not None:
        conditions.append(User.age <= query.max_age)

    return conditions


class UserService:
    def list_users(self, session: Session, query: UserQuery) -> UserPageResponse:
        conditions = build_conditions(query)

        # where(*conditions)：多个表达式默认 AND。
        # 也可以连续 .where(a).where(b)，同样是 AND。
        # 简单 AND 不必强行 and_()；and_() 教学见 query_demo.py。
        stmt = select(User)
        if conditions:
            stmt = stmt.where(*conditions)

        column = SORT_COLUMNS[query.sort_by]
        # order_by：生成 SQL ORDER BY。
        # .asc() / .desc() 挂在 ORM Attribute 上，对应 ASC / DESC。
        # 默认 created_at DESC, id DESC，分页才有稳定顺序。
        # 没有 ORDER BY 时数据库不保证行顺序，翻页可能跳行或重复。
        primary = column.desc() if query.sort_order == "desc" else column.asc()
        stmt = stmt.order_by(primary, User.id.desc())

        # offset：跳过多少行；limit：最多取多少行。
        # 页码：(page - 1) * page_size。主业务用显式 offset/limit，对应 page 更直观。
        # slice(start, stop) 也能变成 LIMIT/OFFSET，教学见 query_demo.py。
        offset = (query.page - 1) * query.page_size
        stmt = stmt.offset(offset).limit(query.page_size)

        items = list(session.execute(stmt).scalars().all())

        # COUNT 必须复用同一套 conditions，且不要带 offset/limit。
        # 列表和 total 筛选不一致时，items 与 total 会对不上。
        # func：构造 SQL 函数表达式；func.count() 生成 COUNT(...)，由数据库完成。
        # 不要先查出全部 ORM 再 len()。
        count_stmt = select(func.count()).select_from(User)
        if conditions:
            count_stmt = count_stmt.where(*conditions)
        # session.scalar(stmt)：只要第一行第一列那个值，适合 COUNT。
        # 和 execute().scalars().all() 拿对象列表不是同一场景。
        total = int(session.scalar(count_stmt) or 0)
        total_pages = 0 if total == 0 else (total + query.page_size - 1) // query.page_size

        return UserPageResponse(
            items=[UserResponse.model_validate(row) for row in items],
            page=query.page,
            page_size=query.page_size,
            total=total,
            total_pages=total_pages,
        )

    def get(self, session: Session, user_id: int) -> User:
        # 主键拿对象：session.get。只要存在性请用 exists，不要为了 True/False 加载整行。
        user = session.get(User, user_id)
        if user is None:
            raise UserNotFoundError(user_id)
        return user

    def email_exists(self, session: Session, email: str) -> bool:
        # exists()：生成 EXISTS 子查询，只问「有没有」，不加载完整 User。
        # 对比：get 拿主键对象；scalar_one_or_none 按业务条件拿单对象；exists 只判断存在。
        stmt = select(exists().where(User.email == email))
        return bool(session.scalar(stmt))
