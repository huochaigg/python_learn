"""V4-03 package 基础：目录 + __init__.py。

学习目标：
1. 理解 package 是「装着多个模块的目录」。
2. 知道 __init__.py 可以当统一出口，类似前端 index.ts。
3. 会写 from demo_package import add。

运行：uv run python lessons/v4/03_package_basics.py
"""

# ---------------------------------------------------------------------------
# demo_package/ 是一个 package，里面有 math_utils.py、string_utils.py。
# 本脚本和 demo_package 在同一目录，所以可以直接 import demo_package。
#
# JS/TS 对比：有点像一个文件夹里多个模块，再用 index.ts 汇总导出。
# ---------------------------------------------------------------------------

# demo_package/__init__.py 里写了：from .math_utils import add
# 所以 add 被重新导出到包这一层。
from demo_package import add

print("from demo_package import add ->", add(2, 3))

# 不经过 __init__.py 再导出时，要写完整模块路径：
from demo_package.string_utils import shout

print("from demo_package.string_utils import shout ->", shout("hello"))

# import 整个包，再用包里重新导出的名字：
import demo_package

print("demo_package.add(10, 1) ->", demo_package.add(10, 1))
# 注意：string_utils 没在 __init__.py 里导出，所以没有 demo_package.shout。

if __name__ == "__main__":
    print("\n--- 03 package 基础 运行完毕 ---")

# 本文件重点：
# 1. 目录组织成 package；学习阶段建议每个包目录保留 __init__.py。
# 2. __init__.py ≈ 前端 index.ts，适合重新导出常用函数。
# 3. from demo_package import add 能成功，是因为 __init__.py 做了再导出。
# 4. 没再导出的模块，就要写成 from demo_package.string_utils import shout。
