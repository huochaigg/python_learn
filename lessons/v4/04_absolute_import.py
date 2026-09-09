"""V4-04 绝对导入：从 package 根开始写完整路径。

学习目标：
1. 看懂 from demo_package.xxx import yyy。
2. 知道绝对导入从「作为顶层包的那个目录」开始写。
3. 理解正式项目为什么更常用绝对导入：路径一眼能看清。

运行：uv run python lessons/v4/04_absolute_import.py
"""

# ---------------------------------------------------------------------------
# 绝对导入
# 它是什么：从顶层 package 名字开始，写出完整模块路径。
# 什么时候用：正式项目里最常见，例如：
#   from app.services.user_service import UserService
# 坑：顶层包叫什么，取决于 Python 从哪找到这个包。
#     本课把 demo_package 放在 lessons/v4/ 下，当前脚本也在这里，
#     所以顶层包名就是 demo_package。
# JS/TS 对比：更像 from "@/app/services/userService" 这种「从项目约定根开始」的导入，
# 而不是 "./" "../" 相对路径。
# ---------------------------------------------------------------------------
from demo_package.math_utils import add, subtract
from demo_package.string_utils import slug
from demo_package.utils.formatter import format_name

print("add(7, 8) =", add(7, 8))
print("subtract(7, 8) =", subtract(7, 8))
print("slug('Hello World') =", slug("Hello World"))
print("format_name('  tom hardy  ') =", format_name("  tom hardy  "))

if __name__ == "__main__":
    print("\n--- 04 绝对导入 运行完毕 ---")

# 本文件重点：
# 1. 绝对导入从 package 根写起：demo_package.utils.formatter。
# 2. 正式项目通常更推荐绝对导入，因为不依赖「当前文件在哪一层」。
# 3. FastAPI 里你会反复看到 from app.xxx import yyy，就是这种。
# 4. 本课脚本能直接 import demo_package，是因为脚本目录就在包旁边。
