"""V6-05 标准库 json：字符串和文件两条线。

学习目标：
1. 分清 dumps/loads（字符串）和 dump/load（文件对象）。
2. 能把 dict 存成 JSON 文件再读回来。
3. 写中文时使用 ensure_ascii=False。

运行：uv run python lessons/v6/05_json.py
"""

from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
USER_JSON = DATA_DIR / "user.json"

user = {
    "name": "汤姆",
    "age": 31,
    "active": True,
}

# ---------------------------------------------------------------------------
# json.dumps(obj, ensure_ascii=True, indent=None)
# 用途：Python 对象 → JSON 字符串。s 可以记成 string。
# 返回值：str。不改原对象，也不写磁盘。
# ensure_ascii=False：中文按中文输出，而不是 \uXXXX。
# indent=2：格式化缩进，方便人读。
# ---------------------------------------------------------------------------
text = json.dumps(user, ensure_ascii=False, indent=2)
print("dumps =\n", text)

# json.loads(s)：JSON 字符串 → Python 对象。返回 dict/list 等。不改文件。
loaded = json.loads(text)
print("loads =", loaded, "name =", loaded["name"])

# ---------------------------------------------------------------------------
# json.dump(obj, file, ...)：Python 对象 → 已打开的文件。
# json.load(file)：已打开的文件 → Python 对象。
# 注意：这两兄弟吃的是文件对象，不是路径字符串。
# 所以仍然要 with open(...) as f。
# ---------------------------------------------------------------------------
with open(USER_JSON, "w", encoding="utf-8") as file:
    json.dump(user, file, ensure_ascii=False, indent=2)

with open(USER_JSON, "r", encoding="utf-8") as file:
    from_file = json.load(file)

print("从文件 load 回来 =", from_file)
print("和原 dict 内容相等 =", from_file == user)

if __name__ == "__main__":
    print("\n--- 05 json 运行完毕 ---")

# 本文件重点：
# 1. dumps/loads 面向字符串；dump/load 面向文件对象。
# 2. dump/load 要配合 with open，并指定 encoding="utf-8"。
# 3. ensure_ascii=False 才能在文件里直接看到中文。
# 4. 非法 JSON 读取会抛 json.JSONDecodeError，下一课会用到。
