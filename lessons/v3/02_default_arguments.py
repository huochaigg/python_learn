"""V3-02 默认参数，以及可变对象当默认值的经典坑。

学习目标：
1. 会写带默认值的函数参数。
2. 记住：不要把 list / dict / set 等可变对象直接当默认参数。
3. 正确写法是默认 None，函数内部再创建新对象。

运行：uv run python lessons/v3/02_default_arguments.py
"""


def hello(name: str = "Tom") -> str:
    """打招呼。name 不传时用 "Tom"。

    参数：name，默认 "Tom"
    返回：问候字符串
    注意：str / int / bool / None 这种不可变默认值是安全的。
    JS/TS 对比：function hello(name = "Tom") 几乎一样。
    """
    return f"Hello, {name}"


print("hello() =", hello())
print("hello('Lucy') =", hello("Lucy"))


# ---------------------------------------------------------------------------
# 错误示例：默认参数用 []。
# 注意：Python 的默认参数只在「函数定义时」求值一次，这个 list 会被反复复用。
# JS/TS 对比：function addItem(item, items = []) 每次调用都会新建数组。
# 这是 Python 和 JS 默认参数最大的行为差异之一。
# ---------------------------------------------------------------------------
def add_item_wrong(item: str, items: list[str] = []) -> list[str]:
    """错误写法：默认 list 会在多次调用之间共享。"""
    items.append(item)
    return items


first_wrong = add_item_wrong("apple")
print("第一次错误调用 =", first_wrong)
second_wrong = add_item_wrong("banana")
print("第二次错误调用 =", second_wrong)
print("两次其实是同一个 list：", first_wrong is second_wrong)


# ---------------------------------------------------------------------------
# 正确写法：默认 None，需要时在函数内部新建 list。
# 每次调用都拿一份新容器，不会串数据。
# ---------------------------------------------------------------------------
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    """正确写法：可变容器不要当默认参数。"""
    if items is None:
        items = []
    items.append(item)
    return items


first = add_item("apple")
second = add_item("banana")
print("第一次正确调用 =", first)
print("第二次正确调用 =", second)
print("两次不是同一个 list：", first is second)

# 如果调用方自己传入 list，仍然是改这份传入的 list（和 JS 引用传递一样）。
bag = ["old"]
add_item("new", bag)
print("调用方传入的 bag =", bag)

if __name__ == "__main__":
    print("\n--- 02 默认参数 运行完毕 ---")

# 本文件重点：
# 1. 不可变默认值（str/int/None）没问题。
# 2. 不要写 def f(items=[]) / def f(data={})，默认对象只创建一次。
# 3. 正确模式：items: list | None = None，函数里 if items is None: items = []。
# 4. JS 默认参数每次调用求值，Python 只在定义时求值一次，不要按 JS 直觉写。
