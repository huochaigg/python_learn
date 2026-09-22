"""
文件作用：用 threading.Lock 模拟循环等待，再用统一加锁顺序对照。第二把锁带 timeout，避免永久卡住。
运行命令：uv run python lessons/v26/deadlock_demo.py
重点概念：Deadlock、circular wait、acquire(timeout)、consistent lock order。
观察重点：交叉加锁时至少一方 timeout；双方都按 lock_a→lock_b 时都能拿到。这是结构模拟，不是数据库行锁。
"""

import threading
from collections.abc import Callable

# threading.Lock：Python 线程互斥锁。这里只借它模拟循环等待结构，
# 不能把它等同于 MySQL/InnoDB 行锁。


def _run_threads(*targets: Callable[[], None]) -> None:
    workers = [threading.Thread(target=fn) for fn in targets]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()


def demo_circular_wait() -> None:
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    got_second: dict[str, bool] = {}
    barrier = threading.Barrier(2)

    def thread_a() -> None:
        print("A acquire lock_a")
        lock_a.acquire()
        barrier.wait()
        print("A wait lock_b")
        # acquire(timeout=...)：最多等 timeout 秒；拿不到返回 False，避免脚本永久卡死。
        got = lock_b.acquire(timeout=1.0)
        got_second["A"] = got
        print(f"A got lock_b={got}")
        if got:
            lock_b.release()
        lock_a.release()

    def thread_b() -> None:
        print("B acquire lock_b")
        lock_b.acquire()
        barrier.wait()
        print("B wait lock_a")
        got = lock_a.acquire(timeout=1.0)
        got_second["B"] = got
        print(f"B got lock_a={got}")
        if got:
            lock_a.release()
        lock_b.release()

    _run_threads(thread_a, thread_b)
    assert got_second["A"] is False or got_second["B"] is False
    print(
        "实际结果总结："
        f"交叉加锁 A.second={got_second['A']} B.second={got_second['B']}，出现 circular wait/timeout。"
    )


def demo_consistent_lock_order() -> None:
    lock_a = threading.Lock()
    lock_b = threading.Lock()
    got_both: dict[str, bool] = {}

    def worker(name: str) -> None:
        print(f"{name} acquire lock_a then lock_b")
        lock_a.acquire()
        got = lock_b.acquire(timeout=1.0)
        got_both[name] = got
        print(f"{name} got lock_b={got}")
        if got:
            lock_b.release()
        lock_a.release()

    _run_threads(lambda: worker("A"), lambda: worker("B"))
    assert got_both["A"] is True and got_both["B"] is True
    print("实际结果总结：统一 lock_a→lock_b 后双方都拿到第二把锁，未形成同样的循环等待。")


def main() -> None:
    demo_circular_wait()
    demo_consistent_lock_order()


if __name__ == "__main__":
    main()
    print("--- v26 deadlock_demo 运行完毕 ---")
