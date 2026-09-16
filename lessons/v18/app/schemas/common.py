"""分页结果对象。Dependency 返回它，endpoint 才能 pagination.page 自动补全。"""

from dataclasses import dataclass


@dataclass
class PaginationParams:
    page: int
    limit: int
    keyword: str | None
