"""简单用户名格式化。"""


def format_name(name: str) -> str:
    """去掉首尾空格并 title case。"""
    return name.strip().title()
