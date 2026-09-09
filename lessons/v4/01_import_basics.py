"""V4-01 标准库 import：import / from ... import / as。

学习目标：
1. 会用三种常见导入写法。
2. 知道 import 之后为什么还要写 math.sqrt。
3. 明确不推荐 from xxx import *。

运行：uv run python lessons/v4/01_import_basics.py
"""

# ---------------------------------------------------------------------------
# import 模块名
# 它是什么：加载一个模块，并在当前文件里留下「模块这个名字」。
# 什么时候用：希望调用时带上模块前缀，避免和本地函数重名。
# 调用方式：math.sqrt(16)，不是 sqrt(16)。
# JS/TS 对比：≈ import * as math from "math"（Python 标准库不写路径、不写扩展名）。
# 注意：这里的 math 是标准库，不是 npm 包，也不需要安装。
# ---------------------------------------------------------------------------
import math

print("math.sqrt(16) =", math.sqrt(16))
print("math.pi =", math.pi)

# ---------------------------------------------------------------------------
# from 模块 import 名字
# 它是什么：只把模块里的某个（些）名字拿到当前作用域。
# 什么时候用：这个名字会反复用，且不容易冲突。
# 调用方式：sqrt(16)，不再写 math.sqrt(16)。
# JS/TS 对比：≈ import { sqrt } from "math"
# 注意：当前文件如果自己也定义了 sqrt，就会覆盖导入的那个。
# ---------------------------------------------------------------------------
from math import sqrt

print("sqrt(9) =", sqrt(9))

# ---------------------------------------------------------------------------
# import 模块 as 别名
# 它是什么：给模块（或导入的名字）换一个更短/更惯用的名字。
# 什么时候用：模块名太长，或项目里约定俗成（以后会看到 import numpy as np）。
# JS/TS 对比：≈ import * as dt from "datetime" / import { sqrt as squareRoot }
# ---------------------------------------------------------------------------
import datetime as dt
from math import sqrt as square_root

print("dt.date(2026, 9, 9) =", dt.date(2026, 9, 9))
print("square_root(25) =", square_root(25))

# ---------------------------------------------------------------------------
# 不推荐：from math import *
# 它会把模块里大量公开名字一次性倒进当前作用域。
# 坑：
# 1. 读代码时看不出 sqrt / pi 从哪来。
# 2. 很容易和本地变量、其他模块的同名函数打架（名字污染）。
# JS/TS 对比：比 import * as math 更糟，因为连命名空间都没有。
# 正式项目请写清楚：import math 或 from math import sqrt。
# ---------------------------------------------------------------------------
# from math import *  # 不要这么写

print("当前文件里能直接用的 sqrt 来自 from math import sqrt")

if __name__ == "__main__":
    print("\n--- 01 标准库 import 运行完毕 ---")

# 本文件重点：
# 1. import math 保留命名空间；from math import sqrt 直接拿名字。
# 2. as 只是起别名，和 JS import alias 一样。
# 3. Python 标准库 import 不写 ./，也不写 .py。
# 4. 不要用 from xxx import *，来源不清、容易重名。
# 5. import 可以分成三类：标准库、第三方包、自己项目。本文件只碰标准库。
