"""V6-06 自定义 Context Manager：__enter__ / __exit__。

学习目标：
1. 知道 with 底层大致依赖 __enter__ 和 __exit__。
2. 能看懂一个最小的资源类。
3. 先理解机制，不展开 contextlib。

运行：uv run python lessons/v6/06_custom_context_manager.py
"""


class DemoResource:
    """假装某种需要获取 / 释放的资源（文件、连接、锁都可以套这个模型）。"""

    def __init__(self, name: str) -> None:
        self.name = name

    def __enter__(self) -> "DemoResource":
        # __enter__：进入 with 时调用。
        # 用途：获取资源（打开文件、拿锁、开始事务）。
        # 返回值：会出现在 as 后面。这里返回 self，所以 as res 就是这个对象。
        print(f"__enter__: 获取 {self.name}")
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        # __exit__：离开 with 时调用，无论成功还是异常。
        # 用途：释放资源（close / rollback / unlock）。
        # 参数：如果代码块里抛错了，会传入异常类型、异常对象、traceback；没抛错则都是 None。
        # 返回值：本课返回 None，表示不吞掉异常。
        # 坑：这里不要展开 traceback 底层；只要知道「退出一定会来这里」。
        print(f"__exit__: 释放 {self.name}, exc_type={exc_type}")

    def work(self) -> str:
        return f"{self.name} is working"


print("=== 正常路径 ===")
with DemoResource("db-session") as res:
    print("with 块内:", res.work())

print("\n=== 异常路径：__exit__ 仍会执行 ===")
try:
    with DemoResource("file-handle") as res:
        print("with 块内即将出错")
        raise ValueError("boom")
except ValueError as e:
    print("外层捕获 =", e)

if __name__ == "__main__":
    print("\n--- 06 自定义 Context Manager 运行完毕 ---")

# 本文件重点：
# 1. 能 with 的对象就是 Context Manager。
# 2. 进入调用 __enter__，退出调用 __exit__。
# 3. 中间抛异常，__exit__ 仍然会跑，这就是 with 比漏写 close 更安全的原因。
# 4. contextlib / yield 写法本版本不学，先记住这两个特殊方法。
