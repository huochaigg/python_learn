"""V6-08 综合练习：用户数据文件管理。

学习目标：
1. 用 Path + with + json 完成读取 / 创建 / 追加 / 保存。
2. 文件不存在时创建；读到坏 JSON 时能捕获。
3. 读回后过滤 active 用户。

运行：uv run python lessons/v6/08_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
USERS_FILE = DATA_DIR / "users.json"


def default_users() -> list[dict]:
    return [
        {"id": 1, "name": "Tom", "active": True},
        {"id": 2, "name": "Jack", "active": False},
    ]


# =============================================================================
# 练习 1
# TODO: 用 Path 打印 USERS_FILE，并判断 exists()。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")
print("USERS_FILE =", USERS_FILE)
print("exists =", USERS_FILE.exists())


# =============================================================================
# 练习 2
# TODO: 写 load_users(path) -> list：
#       不存在则创建默认用户并写回；
#       存在则 with + json.load 读取。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


def load_users(path: Path) -> list[dict]:
    if not path.exists():
        users = default_users()
        path.write_text(
            json.dumps(users, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return users
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data


users = load_users(USERS_FILE)
print("load_users =", users)


# =============================================================================
# 练习 3
# TODO: 若还没有 id=3 的 Lucy，则追加 {"id": 3, "name": "Lucy", "active": True}。
#       用 with + json.dump 保存回文件。反复运行不要重复插入。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")
ids = {user["id"] for user in users}
if 3 not in ids:
    users.append({"id": 3, "name": "Lucy", "active": True})

with USERS_FILE.open("w", encoding="utf-8") as file:
    json.dump(users, file, ensure_ascii=False, indent=2)
print("保存后 users =", users)


# =============================================================================
# 练习 4
# TODO: 再读一次文件，用列表推导式过滤 active 用户，打印他们的 name。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")
with USERS_FILE.open("r", encoding="utf-8") as file:
    saved = json.load(file)
active_names = [user["name"] for user in saved if user["active"]]
print("active names =", active_names)


# =============================================================================
# 练习 5
# TODO: 用 try/except 读取 data/broken.json，捕获 json.JSONDecodeError。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")
broken = DATA_DIR / "broken.json"
try:
    with broken.open("r", encoding="utf-8") as file:
        json.load(file)
except json.JSONDecodeError as e:
    print("JSONDecodeError =", e)


print("---------- 处理结果 ----------")
print("file =", USERS_FILE)
print("all users =", saved)
print("active names =", active_names)

if __name__ == "__main__":
    print("\n--- 08 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 用户数据文件：不存在就创建，存在就 load。
# 2. 修改 list/dict 后必须 dump 回去。
# 3. with + encoding="utf-8" 是文本/JSON 文件的默认姿势。
# 4. 坏 JSON 捕 JSONDecodeError；过滤 active 用推导式即可。
