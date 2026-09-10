"""V6-03 with：自动管理文件生命周期。

学习目标：
1. 看懂手动 open + try/finally + close，以及它和 V5 finally 的关系。
2. 会写 with open(...) as file。
3. 理解 Context Manager 是「资源获取 / 释放」协议。

运行：uv run python lessons/v6/03_with_context.py
"""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
SAMPLE = DATA_DIR / "sample.txt"

print("=== 手动 open + finally close（V5 思路）===")
file = open(SAMPLE, "r", encoding="utf-8")
try:
    print("手动读取第一行 =", repr(file.readline()))
    raise ValueError("假装中途出错")
except ValueError as e:
    print("捕获到 =", e)
finally:
    # 和 V5 一样：无论成功失败都要释放资源。
    file.close()
    print("finally 里已经 close，closed =", file.closed)

print("\n=== with 版本：退出代码块就自动 close ===")
# ---------------------------------------------------------------------------
# with open(...) as file
# 用途：进入时打开资源，离开时自动清理（即使中间抛异常）。
# as file：把 __enter__() 的返回值绑到变量上，这里就是文件对象。
# 是否改文件：取决于 mode；这里 "r" 不改。
# 坑：with 块外面不要再使用 file，它通常已经关闭。
# JS/TS 对比：没有完全对应的日常语法，思想上就是 try/finally 里 resource.close()。
#
# Context Manager：支持 with 的对象。文件对象就是其中一种。
# 它是资源生命周期管理协议：进入获取，退出释放。
# ---------------------------------------------------------------------------
try:
    with open(SAMPLE, "r", encoding="utf-8") as file:
        print("with 内读取 =", repr(file.readline()))
        raise ValueError("with 中间也出错")
except ValueError as e:
    print("捕获到 =", e)

print("离开 with 后 closed =", file.closed)

with open(SAMPLE, "r", encoding="utf-8") as file:
    print("正常 with 读全部 =\n", file.read())
print("正常结束后 closed =", file.closed)

if __name__ == "__main__":
    print("\n--- 03 with / Context Manager 运行完毕 ---")

# 本文件重点：
# 1. 手动 open 必须配 try/finally close，否则异常会漏关文件。
# 2. with open(...) as f 会在离开代码块时自动释放，即使中间报错。
# 3. 实际项目优先 with，不要靠自己记得 close。
# 4. Context Manager = 统一的资源生命周期协议，后面 Session / Lock / HTTP 客户端都会用。
