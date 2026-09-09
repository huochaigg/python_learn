"""V4-02 自定义模块：一个 .py 文件就是一个 module。

学习目标：
1. 会导入同目录下自己写的模块。
2. 分清 import user_utils 和 from user_utils import describe_user。
3. 知道调用时 module.function() 这种写法为什么更不容易重名。

运行：uv run python lessons/v4/02_custom_module.py
"""

# ---------------------------------------------------------------------------
# import 自己的模块
# 同目录下的 user_utils.py 会被当成模块 user_utils。
# JS/TS 对比：
#   import * as userUtils from "./user_utils"
# 差异：Python 这里通常不写 ./，也不写 .py。
# 注意：本文件作为脚本运行时，Python 会把「当前脚本所在目录」放进模块搜索路径，
# 所以同目录的 user_utils.py 能被找到。正式项目更常见的是包路径，见 03/04。
# ---------------------------------------------------------------------------
import user_utils

print("user_utils.normalize_name('  ada  ') =", user_utils.normalize_name("  ada  "))
print("user_utils.is_adult(17) =", user_utils.is_adult(17))
print("user_utils.describe_user('tom', 31) =", user_utils.describe_user("tom", 31))

# ---------------------------------------------------------------------------
# from 自己的模块 import 函数
# 之后可以直接 describe_user(...)，不再写 user_utils. 前缀。
# JS/TS 对比：import { describeUser } from "./user_utils"
# ---------------------------------------------------------------------------
from user_utils import describe_user

print("直接调用 describe_user =", describe_user("lucy", 25))

if __name__ == "__main__":
    print("\n--- 02 自定义模块 运行完毕 ---")

# 本文件重点：
# 1. 一个 .py 文件 ≈ 一个 module。
# 2. import user_utils 之后用 user_utils.xxx()，模块名会保留。
# 3. from user_utils import describe_user 更短，但要小心同名覆盖。
# 4. 自己的模块和标准库写法相同，只是找文件的位置不同。
