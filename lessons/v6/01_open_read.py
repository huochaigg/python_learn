"""V6-01 读文件：open / read / readline / readlines / 逐行迭代。

学习目标：
1. 会用 open() 打开文本文件，并显式指定 encoding="utf-8"。
2. 分清 read / readline / readlines / for line in file。
3. 知道 "r" 模式下文件不存在会抛 FileNotFoundError。

运行：uv run python lessons/v6/01_open_read.py
"""

from pathlib import Path

# 基于当前文件定位 data/，不要写死某台电脑的绝对路径。
DATA_DIR = Path(__file__).resolve().parent / "data"
SAMPLE = DATA_DIR / "sample.txt"

# ---------------------------------------------------------------------------
# open(file, mode="r", encoding=None)
# 用途：打开文件，返回文件对象（文件句柄）。
# 关键参数：
#   file: 路径
#   mode: "r" 只读，文件必须存在
#   encoding: 文本编码。Windows 下不写可能变成系统默认编码，建议显式 utf-8
# 返回值：文件对象，不是字符串。
# 是否改文件：只读模式不改内容。
# 坑：用完必须 close()；中间抛异常时 close 可能跑不到，下一课用 with 解决。
# JS/TS 对比：有点像 fs.openSync / createReadStream，但 Python 文本模式更常用。
# ---------------------------------------------------------------------------
file = open(SAMPLE, "r", encoding="utf-8")
# read()：一次读全部内容，返回 str。
# 坑：大文件不要轻易 read() 全部载入内存。
content = file.read()
print("read() =\n", content)
file.close()

file = open(SAMPLE, "r", encoding="utf-8")
# readline()：读一行（含末尾换行），返回 str。读到文件末尾返回空字符串。
print("readline() 第一次 =", repr(file.readline()))
print("readline() 第二次 =", repr(file.readline()))
file.close()

file = open(SAMPLE, "r", encoding="utf-8")
# readlines()：读所有行，返回 list[str]。每项通常带 \n。
print("readlines() =", file.readlines())
file.close()

print("for line in file:")
file = open(SAMPLE, "r", encoding="utf-8")
# 直接迭代文件对象：逐行读取，大文件更合适。
for line in file:
    print("  ", repr(line))
file.close()

try:
    open(DATA_DIR / "not-exist.txt", "r", encoding="utf-8")
except FileNotFoundError as e:
    print("文件不存在时 FileNotFoundError =", e)

if __name__ == "__main__":
    print("\n--- 01 读文件 运行完毕 ---")

# 本文件重点：
# 1. open(..., "r", encoding="utf-8") 打开只读文本；文件必须存在。
# 2. read 全读，readline 一行，readlines 得到 list，for line 逐行。
# 3. 手动 open 必须 close；异常时可能漏关，下一课用 with。
# 4. Windows 文本读取建议显式 UTF-8。
