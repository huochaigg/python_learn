"""V4-07 import 副作用：顶层代码会在导入时执行。

学习目标：
1. 亲眼看到 import 会执行模块顶层代码。
2. 知道业务逻辑应该放进函数 / 入口，而不是文件一加载就跑。
3. 记住：正式后端项目不要在 import 时写库、发请求、删文件。

运行：uv run python lessons/v4/07_module_side_effect.py
"""

print("准备 import side_effect ...")

# ---------------------------------------------------------------------------
# import 不只是「声明依赖」。
# Python 会加载并执行该模块的顶层代码。
# JS/TS 对比：ESM 顶层代码也会在首次 import 时执行，两边这点其实很像。
# 坑：如果顶层写了发请求 / 写数据库，别人只是想复用一个函数，也会被拖下水。
# ---------------------------------------------------------------------------
import side_effect

print("import 结束。side_effect.LOADED =", side_effect.LOADED)
print("显式调用 side_effect.ping() =", side_effect.ping())

print("\n准备 import clean_module ...")
import clean_module

print("import clean_module 时没有自动 print 业务结果")
print("显式调用 clean_module.ping() =", clean_module.ping())

# 注意：同一进程里再次 import 通常不会把模块顶层再执行一遍（有模块缓存）。
# 这里先知道即可，不必展开 sys.modules。
import side_effect  # 第二次：不会再打印「被 import 了」

print("第二次 import side_effect 不会重复执行顶层 print")

if __name__ == "__main__":
    print("\n--- 07 import 副作用 运行完毕 ---")

# 本文件重点：
# 1. import 会执行模块顶层代码，不只是注册一下名字。
# 2. print / 连库 / 发 HTTP 放在顶层，都算副作用。
# 3. 业务放进函数，启动逻辑放进 if __name__ == "__main__":。
# 4. 正式后端不要让 import 自动写数据库或发请求。
# 5. 同一进程里模块通常只初始化一次。
