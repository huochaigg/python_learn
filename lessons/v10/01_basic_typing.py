"""V10-01 基础类型标注：list[str] / dict[str, int] 等。

学习目标：
1. 会用 Python 3.9+ 内置泛型写法标注容器。
2. 能对应到 TS 的 string[]、Record<string, number>。
3. 记住：普通类型标注默认不做运行时校验。

运行：uv run python lessons/v10/01_basic_typing.py
"""

# ---------------------------------------------------------------------------
# 类型标注：给变量/参数/返回值写上「期望的类型」。
# 用途：给编辑器、pyright/mypy 做静态检查，也方便读代码。
# 运行时：普通 Python 默认不会因为标错类型就立刻报错。
# 以后 Pydantic/FastAPI 会利用 annotation 做额外运行时验证，本课不实现。
# JS/TS 对比：很像 TS 标注，但 TS 编译后类型会擦掉；Python 标注会留在 __annotations__ 里。
# ---------------------------------------------------------------------------

names: list[str] = ["Tom", "Ada"]
# TS 对比：string[]
ages: dict[str, int] = {"Tom": 31, "Ada": 30}
# TS 对比：Record<string, number>
pair: tuple[str, int] = ("Tom", 31)
# TS 对比：[string, number]
ids: set[int] = {1, 2, 3}


def label(name: str, age: int) -> str:
    return f"{name} is {age}"


print("names =", names)
print("ages =", ages)
print("pair =", pair)
print("label =", label("Tom", 31))

# 证明：标注不等于运行时校验。下面这行运行时完全能赋值成功。
# 静态检查工具会报警，但 python 解释器默认不管。
wrong: int = "not-an-int"  # type: ignore[assignment]
print("错误类型仍能跑 =", wrong, type(wrong))

if __name__ == "__main__":
    print("\n--- 01 基础类型标注 运行完毕 ---")

# 本文件重点：
# 1. 现代写法：list[str]、dict[str, int]、tuple[str, int]、set[int]。
# 2. 不必再写 typing.List[str]（旧代码里还能见到）。
# 3. 标注主要服务静态检查，默认不在运行时拦错误类型。
# 4. 和 TS 很像，但职责边界不同：TS 编译期；Python 默认运行时放行。
