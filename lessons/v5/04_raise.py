"""V5-04 raise：主动抛异常，中断正常流程并向上传播。

学习目标：
1. 会在参数校验失败时 raise ValueError。
2. 理解 raise 会立刻离开当前函数，异常交给调用方。
3. 能对比「返回模糊错误值」和「service 主动 raise」。

运行：uv run python lessons/v5/04_raise.py
"""

users = {
    1: {"id": 1, "name": "Tom", "age": 31},
}


def normalize_age(age: int) -> int:
    """年龄非法时主动抛错，而不是返回 -1 / None。

    raise 是什么：主动抛出一个异常对象。
    什么时候用：当前函数没法继续完成承诺（参数非法、状态不对）。
    传播行为：立即中断当前正常流程，跳到最近的 except；没有 except 就继续往上。
    JS/TS 对比：raise ValueError(...) ≈ throw new Error(...)
    后续 FastAPI 中会经常出现：raise HTTPException(status_code=404, detail="...")
    """
    if age < 0:
        raise ValueError("age must be >= 0")
    return age


print("normalize_age(18) =", normalize_age(18))

try:
    normalize_age(-1)
    print("这行到不了")
except ValueError as e:
    print("调用方接到 ValueError =", e)


# ---------------------------------------------------------------------------
# service 风格：找不到就 raise，找到就 return。
# 错误示例：return None，然后每一层都 if result is None。
# 正确示例：本层 raise，由上层统一转换成响应 / 日志。
# ---------------------------------------------------------------------------
def get_user(user_id: int) -> dict[str, int | str]:
    """用户不存在时抛 KeyError（下一课再换成自定义异常）。"""
    if user_id not in users:
        raise KeyError(f"user not found: {user_id}")
    return users[user_id]


print("get_user(1) =", get_user(1))

try:
    get_user(99)
except KeyError as e:
    print("service 主动 raise 后，上层捕获 =", e)

if __name__ == "__main__":
    print("\n--- 04 raise 运行完毕 ---")

# 本文件重点：
# 1. raise 类似 JS throw，会立刻中断当前函数。
# 2. 明显的业务条件（age < 0）应该先判断再 raise，不要靠制造崩溃来控流程。
# 3. service 更常见：不存在 / 不合法 → raise；正常 → return。
# 4. 异常不处理就会一直向上传播，直到被 except 或撑破程序。
