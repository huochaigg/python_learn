"""V4-05 相对导入：. 和 ..，以及为什么要用 python -m。

学习目标：
1. 理解 . 是当前包，.. 是上一级包。
2. 知道相对导入基于 package，不完全等于磁盘上的 ../。
3. 知道直接 python xxx.py 跑包内模块可能报 no known parent package。
4. 会用 python -m package.module 按模块运行。

运行：
  uv run python lessons/v4/05_relative_import.py
  uv run --directory lessons/v4 python -m demo_package.services.user_service
"""

from pathlib import Path
import subprocess
import sys

# ---------------------------------------------------------------------------
# 相对导入写在包内部的模块里，而不是写在本课这种「顶层脚本」里。
# 本脚本如果写 from .demo_package import add，会失败：
# 它自己不是 package 里的模块。
#
# 真正的相对导入在：
#   demo_package/services/user_service.py
#   from ..utils.formatter import format_name
#   from ..math_utils import add
#
# .  = demo_package.services（当前包）
# .. = demo_package（上一级包）
#
# JS/TS 对比：看起来像 import from "../utils/formatter"
# 差异：Python 相对导入要求「当前文件是某个 package 的一部分」。
#       直接当脚本跑时，它常常没有 parent package。
# ---------------------------------------------------------------------------

# 通过绝对导入把带相对导入的模块「作为 package 的一部分」加载进来。
# 这时 user_service 里的 from ..utils.formatter import ... 是可以成功的。
from demo_package.services.user_service import create_user

print("作为 package 被 import 时，相对导入可用")
print("create_user('  lucy  ', 20) =", create_user("  lucy  ", 20))

# ---------------------------------------------------------------------------
# python -m 按模块运行
# 它是什么：告诉 Python「把这个点分路径当成 module/package 来执行」。
# 什么时候用：入口在包内部、文件里还有相对导入。
# 坑：python demo_package/services/user_service.py 往往会 ImportError。
# JS/TS 对比：有点像必须从项目根按包名启动，而不是双击运行某个深层 src 文件。
# ---------------------------------------------------------------------------
print("\n接下来用 python -m 运行包内模块（工作目录 = lessons/v4）")
sys.stdout.flush()
v4_dir = Path(__file__).resolve().parent
result = subprocess.run(
    [sys.executable, "-m", "demo_package.services.user_service"],
    cwd=v4_dir,
    check=True,
)
print("-m 子进程退出码 =", result.returncode)

print("\n错误示范（不要依赖这种跑法）：")
print("  uv run python lessons/v4/demo_package/services/user_service.py")
print("正确示范（项目根目录执行）：")
print("  uv run --directory lessons/v4 python -m demo_package.services.user_service")

if __name__ == "__main__":
    print("\n--- 05 相对导入 运行完毕 ---")

# 本文件重点：
# 1. . 当前包，.. 上一级包；它基于 package 结构。
# 2. 相对导入写在包内模块里；顶层脚本自己不能 from .xxx import。
# 3. 直接 python 包内文件.py 容易报 no known parent package。
# 4. 包内入口用 python -m package.module。
# 5. 被别人按 package import 时，相对导入是正常的。
