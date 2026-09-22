"""
文件作用：对比 READ COMMITTED 与 snapshot 两种读模型下，同一行两次读取是否变化。
运行命令：uv run python lessons/v26/non_repeatable_read_demo.py
重点概念：Non-repeatable Read、READ COMMITTED、snapshot/repeatable。
观察重点：RC 下 A 先 100 后 50；snapshot 下 A 两次都是 100。这是可执行概念模型，不是 SQLite 内核隔离实验。
"""


class CommittedStore:
    def __init__(self, value: int) -> None:
        self.value = value

    def read(self) -> int:
        return self.value

    def commit_write(self, value: int) -> None:
        self.value = value


class SnapshotReader:
    def __init__(self, store: CommittedStore) -> None:
        # Non-repeatable Read 看的是已有行的字段值变化，不是结果集多了一行。
        self.snapshot = store.read()

    def read(self) -> int:
        return self.snapshot


def demo_read_committed_non_repeatable_read() -> None:
    store = CommittedStore(100)
    first = store.read()
    store.commit_write(50)
    second = store.read()
    assert first == 100
    assert second == 50
    print(f"实际结果总结：READ COMMITTED 模拟：A 第一次={first}，第二次={second}，因此发生不可重复读。")


def demo_repeatable_snapshot() -> None:
    store = CommittedStore(100)
    reader_a = SnapshotReader(store)
    first = reader_a.read()
    store.commit_write(50)
    second = reader_a.read()
    assert first == 100
    assert second == 100
    assert store.read() == 50
    print(f"实际结果总结：snapshot 模拟：A 第一次={first}，第二次={second}，本事务内可重复。")


def main() -> None:
    demo_read_committed_non_repeatable_read()
    demo_repeatable_snapshot()


if __name__ == "__main__":
    main()
    print("--- v26 non_repeatable_read_demo 运行完毕 ---")
