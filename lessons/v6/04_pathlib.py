"""V6-04 pathlib.Path：用对象而不是手拼路径字符串。

学习目标：
1. 会用 Path(__file__) 定位当前文件旁边的目录。
2. 会用 / 拼接路径，并用 exists / is_file 判断。
3. 会用 mkdir / read_text / write_text 做最常见的文件操作。

运行：uv run python lessons/v6/04_pathlib.py
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Path(...)：把路径变成对象。
# 用途：跨平台处理路径（Windows 的 \ 和 POSIX 的 / 都交给它）。
# 返回值：Path 对象，不是立刻读文件。
# 是否改文件系统：仅构造 Path 不会。
# JS/TS 对比：≈ path.join / path.resolve 得到的路径对象，再配合 fs。
# ---------------------------------------------------------------------------
here = Path(__file__).resolve()
data_dir = here.parent / "data"
# / 运算符：拼接路径，返回新的 Path。不会改磁盘。
# JS/TS 对比：≈ path.join(parent, "data", "path_demo.txt")
demo_file = data_dir / "path_demo.txt"
sub_dir = data_dir / "subdir"

print("当前文件 =", here)
print("data 目录 =", data_dir)
print("拼接后的文件 =", demo_file)

# exists()：路径是否存在。返回 bool。不改文件系统。
# is_file()：是否是普通文件。返回 bool。目录存在时 is_file() 为 False。
print("data_dir.exists() =", data_dir.exists())
print("demo_file.exists() 写入前 =", demo_file.exists())
print("sample.txt is_file() =", (data_dir / "sample.txt").is_file())

# mkdir(parents=True, exist_ok=True)
# 用途：创建目录。返回 None。
# 会改文件系统：是。
# parents=True 相当于 mkdir -p；exist_ok=True 表示已存在不报错。
sub_dir.mkdir(parents=True, exist_ok=True)
print("subdir 已确保存在 =", sub_dir.exists())

# write_text(data, encoding="utf-8")：把字符串写入文件。
# 返回值：写入的字符数。会覆盖已有文件（类似 mode="w"）。
# 会改文件系统：是。
n = demo_file.write_text("from pathlib\n第二行\n", encoding="utf-8")
print("write_text 写入字符数 =", n)

# read_text(encoding="utf-8")：读全部文本，返回 str。不改文件内容。
# 坑：同样是一次性读入内存，大文件要谨慎。
print("read_text =\n", demo_file.read_text(encoding="utf-8"))
print("写入后 exists / is_file =", demo_file.exists(), demo_file.is_file())

if __name__ == "__main__":
    print("\n--- 04 pathlib 运行完毕 ---")

# 本文件重点：
# 1. 路径处理优先 Path，少用字符串手拼。
# 2. Path(__file__).parent / "data" 能保证从项目根运行也找得到文件。
# 3. exists / is_file 只查询；mkdir / write_text 会改磁盘。
# 4. read_text / write_text 适合小文本；底层仍然建议 UTF-8。
