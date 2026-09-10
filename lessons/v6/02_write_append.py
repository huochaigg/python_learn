"""V6-02 写文件：w 覆盖、a 追加、write / writelines。

学习目标：
1. 分清 "w" 覆盖和 "a" 追加。
2. 知道 write() 不会自动加换行。
3. 所有演示只操作 lessons/v6/data/ 下的测试文件。

运行：uv run python lessons/v6/02_write_append.py
"""

from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
WRITE_FILE = DATA_DIR / "write_demo.txt"
APPEND_FILE = DATA_DIR / "append_demo.txt"

# ---------------------------------------------------------------------------
# mode="w"：写入。文件不存在会创建；已存在会清空后重写（覆盖）。
# 坑：手滑用 "w" 打开重要文件，原内容就没了。本课只写 data/ 测试文件。
# ---------------------------------------------------------------------------
file = open(WRITE_FILE, "w", encoding="utf-8")
# write(text)：把字符串写入文件，返回写入的字符数。
# 注意：不会自动添加 \n，需要换行就自己写。
# 是否改文件：会。
written = file.write("first line")
print("write() 返回字符数 =", written)
file.write("\nsecond line\n")
file.close()

file = open(WRITE_FILE, "r", encoding="utf-8")
print("覆盖写入后的内容 =\n", file.read())
file.close()

# 再 "w" 一次：旧内容会被清掉。
file = open(WRITE_FILE, "w", encoding="utf-8")
# writelines(lines)：写入一组字符串。同样不会自动给每项补 \n。
file.writelines(["alpha\n", "beta\n"])
file.close()

file = open(WRITE_FILE, "r", encoding="utf-8")
print("再次 w 之后（旧内容已覆盖）=\n", file.read())
file.close()

# ---------------------------------------------------------------------------
# mode="a"：追加到末尾，不覆盖旧内容；文件不存在会创建。
# ---------------------------------------------------------------------------
file = open(APPEND_FILE, "w", encoding="utf-8")
file.write("old\n")
file.close()

file = open(APPEND_FILE, "a", encoding="utf-8")
file.write("new\n")
file.close()

file = open(APPEND_FILE, "r", encoding="utf-8")
print("追加后的内容 =\n", file.read())
file.close()

if __name__ == "__main__":
    print("\n--- 02 写文件 运行完毕 ---")

# 本文件重点：
# 1. "w" 覆盖；"a" 追加；文件不存在时两者都会创建。
# 2. write / writelines 都不会自动加换行。
# 3. 只对 data/ 测试文件动手，不要拿 "w" 去开真实重要文件。
# 4. 本课仍手动 close，下一课改成 with。
