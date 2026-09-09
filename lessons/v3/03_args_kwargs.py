"""V3-03 *args 与 **kwargs：定义时收集，调用时展开。

学习目标：
1. *args 收集多余位置参数，变成 tuple。
2. **kwargs 收集多余关键字参数，变成 dict。
3. 调用时 *list 展开位置参数，**dict 展开关键字参数。
4. 记住：定义阶段是收集，调用阶段是展开。

运行：uv run python lessons/v3/03_args_kwargs.py
"""


# ---------------------------------------------------------------------------
# *args：接收任意数量的位置参数，收集成 tuple。
# 参数：任意多个位置值。返回：本例返回求和结果。不修改调用方数据。
# JS/TS 对比：function add(...args) 很像，但 JS 的 rest 是数组，Python 的 args 是 tuple。
# 注意：名字写成 args 只是约定，星号 * 才是语法；写成 *numbers 也可以。
# ---------------------------------------------------------------------------
def add(*args: int) -> int:
    """把所有位置参数加起来。"""
    print("  *args 收集到的 tuple =", args, "类型 =", type(args))
    return sum(args)


print("add(1, 2, 3) =", add(1, 2, 3))
print("add(10) =", add(10))


# ---------------------------------------------------------------------------
# **kwargs：接收任意数量的关键字参数，收集成 dict。
# JS/TS 对比：JS 没有「把命名参数扫进对象」的语言级语法，通常直接收一个 options 对象。
# 注意：* 和 ** 是两套语义。
#   *   管位置参数 / 序列展开
#   **  管关键字参数 / 字典展开
# JS 的 ... 在数组和对象上都能用，Python 必须选对 * 还是 **。
# ---------------------------------------------------------------------------
def create_user(**kwargs) -> dict:
    """把关键字参数原样收成 dict 返回。"""
    print("  **kwargs 收集到的 dict =", kwargs, "类型 =", type(kwargs))
    return kwargs


print("create_user(name='Tom', age=31) =", create_user(name="Tom", age=31))


# ---------------------------------------------------------------------------
# 调用阶段：*list 展开位置参数。
# add(*nums) 等价于 add(1, 2, 3)
# 定义里的 *args 是收集；这里的 *nums 是展开。
# JS/TS 对比：add(...nums)
# ---------------------------------------------------------------------------
nums = [1, 2, 3]
print("add(*nums) =", add(*nums))


# ---------------------------------------------------------------------------
# 调用阶段：**dict 展开关键字参数。
# create_user(**data) 等价于 create_user(name="Tom", age=31)
# 后续 FastAPI 中会经常出现：User(**data)、model_validate 前后的 dict 展开。
# JS/TS 对比：没有完全对应语法；更像 createUser({ ...data })。
# ---------------------------------------------------------------------------
data = {"name": "Tom", "age": 31}
print("create_user(**data) =", create_user(**data))


# 也可以两种一起用：前面收集位置，后面收集关键字。
def log_call(*args, **kwargs) -> None:
    """通用日志函数：位置参数进 args，关键字参数进 kwargs。"""
    print("  args =", args, "kwargs =", kwargs)


log_call(1, 2, level="info", source="v3")

if __name__ == "__main__":
    print("\n--- 03 *args **kwargs 运行完毕 ---")

# 本文件重点：
# 1. *args 收集成 tuple；**kwargs 收集成 dict。
# 2. 函数定义时 * / ** 是收集；函数调用时 * / ** 是展开。
# 3. Python 的 * 和 ** 不能混用语义，不像 JS 一个 ... 通吃。
# 4. User(**data) 就是调用阶段的字典展开，V2 的 **user 和这里是同一套语法。
