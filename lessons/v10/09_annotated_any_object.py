"""V10-09 Annotated / Any / object。

学习目标：
1. 眼熟 Annotated[类型, metadata] 这种「类型 + 附加信息」。
2. 分清 Any 会大幅放宽检查，object 仍然很严。
3. 知道以后 FastAPI 会写成 Annotated[str, Query(...)]，本课只认结构。

运行：uv run python lessons/v10/09_annotated_any_object.py
"""

from typing import Annotated, Any


# ---------------------------------------------------------------------------
# Annotated[T, metadata...]
# 是什么：在类型 T 上再挂一些元数据。
# 用途：给框架看（校验、Query、依赖注入），静态类型仍然按 T 来。
# 本课 metadata 只用字符串，不安装 FastAPI。
# 以后会出现：Annotated[str, Query(min_length=1)]
# 运行时：普通 Python 默认不解读这些 metadata。
# ---------------------------------------------------------------------------
UserName = Annotated[str, "min_length=2", "path_param"]


def hello(name: UserName) -> str:
    return f"Hello, {name}"


print("Annotated 实际还是当 str 用 =", hello("Ada"))

# ---------------------------------------------------------------------------
# Any：关闭精细检查，几乎随便传、随便用。
# TS 对比：粗略像 any，但不是完全等价。
# 坑：一用 Any，类型系统就帮不上什么忙。能写清就别用。
#
# object：所有类型的根，值可以是任何对象，但使用具体属性前要先收窄类型。
# TS 对比：更接近 unknown，同样不是 100% 等同。
# ---------------------------------------------------------------------------

def accept_any(value: Any) -> str:
    # 静态检查几乎不管你对 value 做什么。
    return str(value)


def accept_object(value: object) -> str:
    # 这里直接 value.upper() 通常会被类型检查拒绝。
    # 运行时若真是 str 就能跑；检查器希望你先 isinstance。
    if isinstance(value, str):
        return value.upper()
    return str(value)


print("Any =", accept_any(123))
print("object 收窄后 =", accept_object("tom"))

if __name__ == "__main__":
    print("\n--- 09 Annotated / Any / object 运行完毕 ---")

# 本文件重点：
# 1. Annotated 是「类型 + metadata」，FastAPI 会大量用，现在先眼熟。
# 2. Any 很宽，应谨慎；object 要求先判断再当具体类型用。
# 3. 它们都不是 Pydantic 那种运行时验证器。
# 4. TS any/unknown 只能当直觉类比，不要一一硬套。
