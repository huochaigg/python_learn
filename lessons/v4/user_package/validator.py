"""简单用户名校验。"""


def is_valid_name(name: str) -> bool:
    """非空、去掉空格后长度至少 2。"""
    cleaned = name.strip()
    return len(cleaned) >= 2
