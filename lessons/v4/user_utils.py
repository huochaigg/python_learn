"""自定义模块：给 02_custom_module.py 导入用。

一个 .py 文件就是一个 module。
JS/TS 对比：≈ userUtils.ts 这种本地模块文件。
"""


def normalize_name(name: str) -> str:
    """去掉首尾空格并转成首字母大写。"""
    return name.strip().title()


def is_adult(age: int) -> bool:
    """年龄是否 >= 18。"""
    return age >= 18


def describe_user(name: str, age: int) -> str:
    """拼一句用户描述。"""
    status = "adult" if is_adult(age) else "minor"
    return f"{normalize_name(name)} is {status}"
