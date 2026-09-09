"""demo_package 里的字符串小工具。"""


def shout(text: str) -> str:
    """变成大写。"""
    return text.upper()


def slug(text: str) -> str:
    """空格换成短横线，并转小写。"""
    return "-".join(text.strip().lower().split())
