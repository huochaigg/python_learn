"""
文件作用：用 SharedStore/Transaction 模拟脏读：B 读到 A 未提交值，A rollback 后 committed_value 不变。
运行命令：uv run python lessons/v26/dirty_read_demo.py
重点概念：Dirty Read、uncommitted_value、rollback。
观察重点：B 在 READ UNCOMMITTED 下读到 50；A rollback 后 committed_value 仍是 100。这是概念模拟，不是 SQLite 真实隔离。
"""


class SharedStore:
    def __init__(self, committed_value: int) -> None:
        self.committed_value = committed_value
        self.uncommitted_value: int | None = None


class Transaction:
    def __init__(self, store: SharedStore, isolation: str) -> None:
        self.store = store
        self.isolation = isolation

    def write(self, value: int) -> None:
        self.store.uncommitted_value = value

    def read(self) -> int:
        # Dirty Read：READ UNCOMMITTED 允许读到别人尚未提交的值。
        if self.isolation == "READ UNCOMMITTED" and self.store.uncommitted_value is not None:
            return self.store.uncommitted_value
        return self.store.committed_value

    def rollback(self) -> None:
        self.store.uncommitted_value = None

    def commit(self) -> None:
        if self.store.uncommitted_value is not None:
            self.store.committed_value = self.store.uncommitted_value
        self.store.uncommitted_value = None


def demo_dirty_read() -> None:
    store = SharedStore(committed_value=100)
    tx_a = Transaction(store, isolation="READ COMMITTED")
    tx_b = Transaction(store, isolation="READ UNCOMMITTED")

    tx_a.write(50)
    dirty = tx_b.read()
    tx_a.rollback()

    assert dirty == 50
    assert store.committed_value == 100
    assert store.uncommitted_value is None
    print("实际结果总结：B 脏读到 50；A rollback 后 committed_value 仍是 100。")


def main() -> None:
    demo_dirty_read()


if __name__ == "__main__":
    main()
    print("--- v26 dirty_read_demo 运行完毕 ---")
