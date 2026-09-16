"""当前模拟用户。不是 JWT payload，只为看清 dependency 往下传对象。"""

from dataclasses import dataclass


@dataclass
class CurrentUser:
    id: int
    name: str
    role: str
