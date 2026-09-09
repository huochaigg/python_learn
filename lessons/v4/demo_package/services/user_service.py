"""用相对导入调用同包里的其他模块。

相对导入基于 package，不是单纯的磁盘相对路径：
- .  表示当前包（这里是 demo_package.services）
- .. 表示上一级包（这里是 demo_package）

所以：
  from ..utils.formatter import format_name
等价于从 demo_package.utils.formatter 拿 format_name。

注意：
直接运行本文件可能报：
  ImportError: attempted relative import with no known parent package
因为 python xxx.py 会把它当普通脚本，不一定知道它属于哪个 package。

正确运行（在项目根目录）：
  uv run --directory lessons/v4 python -m demo_package.services.user_service

python -m 的意思：按「模块/包」来运行，而不是把某个 .py 当孤立脚本。
"""

from ..utils.formatter import format_name
from ..math_utils import add


def create_user(name: str, score: int) -> dict[str, str | int]:
    """格式化名字，并把 score + 1 当作初始积分。"""
    return {
        "name": format_name(name),
        "score": add(score, 1),
    }


if __name__ == "__main__":
    print("user_service 作为模块入口运行")
    print("create_user('  ada  ', 10) =", create_user("  ada  ", 10))
