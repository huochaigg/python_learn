"""V5-06 重新抛出与异常链。

学习目标：
1. 会在 except 里记一笔日志，再把异常继续抛上去。
2. 记住：重新抛当前异常优先直接 raise，而不是 raise e。
3. 眼熟 raise NewError(...) from e，知道它在保留因果。

运行：uv run python lessons/v5/06_reraise_and_chain.py
"""


class UserDataError(Exception):
    """把底层解析错误包装成业务一点的异常。"""


def parse_age(raw: str) -> int:
    return int(raw)


def load_age(raw: str) -> int:
    """service 层：接住底层异常，记录后原样再抛出去。"""
    try:
        return parse_age(raw)
    except ValueError as e:
        print("  [log] 解析年龄失败:", e)
        # raise（单独一个）：把当前正在处理的异常原样继续抛出去。
        # 用途：本层只想记日志 / 加上下文，真正怎么处理交给上层。
        # 注意：重新抛当前异常优先写 raise，不要写 raise e。
        # raise e 也能抛，但 traceback / 异常链不如直接 raise 完整。
        # 现在不必抠底层差异，先记住这个习惯。
        raise


print("load_age('18') =", load_age("18"))

try:
    load_age("abc")
except ValueError as e:
    print("上层仍然收到原来的 ValueError =", e)


def load_age_wrapped(raw: str) -> int:
    """把底层 ValueError 转成 UserDataError，同时保留因果。"""
    try:
        return parse_age(raw)
    except ValueError as e:
        # raise NewError(...) from e
        # 它是什么：抛一个新异常，并声明「它是由 e 导致的」。
        # 什么时候用：底层错误太技术，上层想换成业务异常，但排障还要看到根因。
        # 本课先眼熟，不要求把 traceback 细节背下来。
        raise UserDataError(f"invalid age: {raw}") from e


try:
    load_age_wrapped("abc")
except UserDataError as e:
    print("上层收到 UserDataError =", e)
    print("  __cause__（底层原因）=", e.__cause__)

if __name__ == "__main__":
    print("\n--- 06 重新抛出 / 异常链 运行完毕 ---")

# 本文件重点：
# 1. except 里先 log，再 raise，异常会继续往上走。
# 2. 重新抛当前异常优先直接 raise，而不是 raise e。
# 3. raise UserDataError(...) from e 保留「业务异常由哪个底层异常导致」。
# 4. 这版看懂形态即可，不必深挖 traceback。
