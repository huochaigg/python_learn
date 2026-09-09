"""V5-08 综合练习：try / 多 except / else / finally / raise / 自定义异常 / 重新抛出。

学习目标：
1. 把本版语法串到 user/order 小场景里。
2. 先在 TODO 自己写，再看示例答案。
3. 打断点观察异常是从哪抛、在哪被捕获的。

运行：uv run python lessons/v5/08_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""


class BizException(Exception):
    """业务异常基类。"""


class UserNotFoundError(BizException):
    """用户不存在。"""


USERS: dict[str, dict[str, int | str]] = {
    "u1": {"id": "u1", "name": "Tom", "age": 31},
    "u2": {"id": "u2", "name": "Jack", "age": 17},
}


# =============================================================================
# 练习 1
# TODO: 写 parse_age(raw: str) -> int，用 int(raw) 转换。
#       用 try / except ValueError 调用 parse_age("18") 和 parse_age("abc")。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


def parse_age(raw: str) -> int:
    return int(raw)


for raw in ["18", "abc"]:
    try:
        print(f"parse_age({raw!r}) =", parse_age(raw))
    except ValueError as e:
        print(f"ValueError: {e}")


# =============================================================================
# 练习 2
# TODO: 写 get_user(user_id: str)，找不到 raise UserNotFoundError。
#       分别捕获 UserNotFoundError 和 KeyError 是不够的——这里应只抛自定义异常。
#       再写一个 get_field(user, key) 用 user[key]，对缺键捕获 KeyError。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")


def get_user(user_id: str) -> dict[str, int | str]:
    user = USERS.get(user_id)
    if user is None:
        raise UserNotFoundError(f"user not found: {user_id}")
    return user


def get_field(user: dict[str, int | str], key: str) -> int | str:
    return user[key]


try:
    print("get_user('u1') =", get_user("u1"))
    print("city =", get_field(get_user("u1"), "city"))
except UserNotFoundError as e:
    print("UserNotFoundError =", e)
except KeyError as e:
    print("KeyError =", e)

try:
    get_user("missing")
except UserNotFoundError as e:
    print("UserNotFoundError =", e)
except KeyError as e:
    print("KeyError =", e)


# =============================================================================
# 练习 3
# TODO: 解析 parse_age("20")，成功走 else 打印成年判断，无论成败 finally 打印 done。
#       再对 parse_age("x") 走一遍，确认 else 不执行、finally 仍执行。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")
for raw in ["20", "x"]:
    try:
        age = parse_age(raw)
    except ValueError as e:
        print(f"raw={raw!r} except {e}")
    else:
        print(f"raw={raw!r} else adult={age >= 18}")
    finally:
        print(f"raw={raw!r} finally done")


# =============================================================================
# 练习 4
# TODO: 写 require_adult(age: int) -> int，age < 18 时 raise ValueError。
# =============================================================================
print("\n===== 练习 4 TODO =====")


print("===== 练习 4 示例答案 =====")


def require_adult(age: int) -> int:
    if age < 18:
        raise ValueError("user is not adult")
    return age


try:
    print("require_adult(31) =", require_adult(31))
    require_adult(17)
except ValueError as e:
    print("ValueError =", e)


# =============================================================================
# 练习 5
# TODO: 写 load_user_age(user_id: str) -> int：
#       内部调用 get_user；若 UserNotFoundError，先 print log，再直接 raise。
# =============================================================================
print("\n===== 练习 5 TODO =====")


print("===== 练习 5 示例答案 =====")


def load_user_age(user_id: str) -> int:
    try:
        user = get_user(user_id)
    except UserNotFoundError as e:
        print("  [log] load_user_age failed:", e)
        raise
    return int(user["age"])


print("load_user_age('u1') =", load_user_age("u1"))
try:
    load_user_age("missing")
except UserNotFoundError as e:
    print("上层仍收到 UserNotFoundError =", e)


# =============================================================================
# 练习 6
# TODO: 对 ["u1", "u2", "missing"] 调用 load_user_age + require_adult，
#       分别处理 UserNotFoundError 和 ValueError，最后打印摘要。
# =============================================================================
print("\n===== 练习 6 TODO =====")


print("===== 练习 6 示例答案 =====")
summary: list[str] = []
for user_id in ["u1", "u2", "missing"]:
    try:
        age = load_user_age(user_id)
        require_adult(age)
    except UserNotFoundError as e:
        summary.append(f"{user_id}: 404 {e}")
    except ValueError as e:
        summary.append(f"{user_id}: 400 {e}")
    else:
        summary.append(f"{user_id}: 200 adult")
    finally:
        pass

print("---------- 处理结果 ----------")
for line in summary:
    print(line)

if __name__ == "__main__":
    print("\n--- 08 综合练习 运行完毕 ---")

# 本文件重点：
# 1. 具体 except 分流：ValueError 参数问题，UserNotFoundError 业务问题。
# 2. else / finally 分别负责成功后续和收尾。
# 3. 找不到用户 raise 自定义异常，不要返回 None。
# 4. 重新抛当前异常用单独的 raise。
# 5. 不要 except: pass，也不要所有失败都装进一个 ValueError。
