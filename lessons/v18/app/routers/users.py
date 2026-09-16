"""用户接口：复用分页依赖 + admin 依赖链。"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from lessons.v18.app.dependencies.auth import require_admin
from lessons.v18.app.dependencies.common import PaginationDep
from lessons.v18.app.schemas.user import CurrentUser

router = APIRouter(prefix="/users", tags=["users"])

_users: list[dict[str, Any]] = [
    {"id": 1, "name": "Ada"},
    {"id": 2, "name": "Tom"},
    {"id": 3, "name": "Jack"},
]


@router.get("")
def list_users(pagination: PaginationDep) -> dict[str, Any]:
    print(f"pagination: {pagination}")
    # PaginationDep = Annotated[PaginationParams, Depends(get_pagination)]
    # users / orders 共用同一个 dependency，Swagger 里也会出现 page/limit/keyword。
    # 老写法对照（本课不用）：pagination: PaginationParams = Depends(get_pagination)
    start = (pagination.page - 1) * pagination.limit
    items = _users
    if pagination.keyword:
        items = [row for row in items if pagination.keyword.lower() in row["name"].lower()]
    return {
        "page": pagination.page,
        "limit": pagination.limit,
        "items": items[start : start + pagination.limit],
    }


@router.get("/admin-only")
def admin_only(user: Annotated[CurrentUser, Depends(require_admin)]) -> dict[str, Any]:
    # 依赖链：Request → get_token → get_current_user → require_admin → 本函数。
    # 看终端 print 顺序。Header 用 X-Token: admin-token。
    print("[dep] 4 endpoint admin_only")
    return {"ok": True, "user": user.name, "role": user.role}
