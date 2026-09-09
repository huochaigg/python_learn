"""demo_package.utils 里的格式化工具，给相对导入演示用。"""


def format_name(name: str) -> str:
    """去掉首尾空格，并把每个单词首字母大写。"""
    return name.strip().title()
