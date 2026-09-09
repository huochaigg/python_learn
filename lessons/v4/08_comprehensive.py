"""V4-08 综合练习：自定义模块、package、__init__.py、绝对导入、入口函数。

学习目标：
1. 自己写 import，把 user_utils 和 user_package 串起来。
2. 用绝对导入和包再导出各写一次。
3. 用 main() + if __name__ == "__main__": 做入口。

运行：uv run python lessons/v4/08_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

# =============================================================================
# 练习 1
# TODO: 导入同目录自定义模块 user_utils，打印 describe_user("  tom  ", 31)
# 提示：import user_utils
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")
import user_utils

print(user_utils.describe_user("  tom  ", 31))


# =============================================================================
# 练习 2
# TODO: 用绝对导入从包内模块拿函数：
#       from user_package.formatter import format_name
#       from user_package.validator import is_valid_name
#       打印 format_name("  lucy  ") 和 is_valid_name("A")
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")
from user_package.formatter import format_name
from user_package.validator import is_valid_name

print("format_name =", format_name("  lucy  "))
print("is_valid_name('A') =", is_valid_name("A"))
print("is_valid_name('Ada') =", is_valid_name("Ada"))


# =============================================================================
# 练习 3
# TODO: 走 __init__.py 的统一出口：from user_package import format_name as fmt
#       确认 fmt(" jack ") 和练习 2 的 format_name 是同一个函数。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")
from user_package import format_name as fmt

print("fmt(' jack ') =", fmt(" jack "))
print("fmt is format_name =", fmt is format_name)


# =============================================================================
# 练习 4
# TODO: 写 process_user(name: str) -> str：
#       非法名字返回 "invalid"；合法则返回 format 后的名字。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


def process_user(name: str) -> str:
    """先校验，再格式化。"""
    if not is_valid_name(name):
        return "invalid"
    return format_name(name)


print("process_user('  mike  ') =", process_user("  mike  "))
print("process_user(' ') =", process_user(" "))


# =============================================================================
# 练习 5
# TODO: 写 main()，批量处理 ["  ada  ", "b", "Lucy"] 并打印。
#       用 if __name__ == "__main__": 调用 main()。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")


def main() -> None:
    names = ["  ada  ", "b", "Lucy"]
    for name in names:
        print(repr(name), "->", process_user(name))


if __name__ == "__main__":
    main()
    print("\n--- 08 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 同目录 .py 可当自定义 module 直接 import。
# 2. from user_package.formatter import xxx 是绝对导入。
# 3. __init__.py 再导出后，可以从包根 import 常用函数。
# 4. 入口逻辑放进 main()，用 if __name__ == "__main__": 启动。
# 5. 这些就是后面 FastAPI 项目 from app.services.xxx import yyy 的缩影。
