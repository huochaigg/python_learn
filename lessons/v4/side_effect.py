"""演示：模块顶层代码会在 import 时执行。"""

print("side_effect.py 被 import 了，这条 print 就是副作用")

LOADED = True


def ping() -> str:
    """真正的业务功能，应该由调用方显式执行。"""
    return "pong"
