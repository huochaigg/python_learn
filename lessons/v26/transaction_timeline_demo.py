"""
文件作用：用状态对象串联 V23 原子性、V24 丢失更新、V26 可见性，而不是只打印讲义。
运行命令：uv run python lessons/v26/transaction_timeline_demo.py
重点概念：原子性 vs 怎么改同一行 vs 彼此能看见什么。
观察重点：Transaction、Lost Update、Isolation/Snapshot 解决的是不同问题。
"""


class Ledger:
    def __init__(self, stock: int) -> None:
        self.stock = stock
        self.order_created = False

    def snapshot(self) -> tuple[int, bool]:
        return (self.stock, self.order_created)


def demo_v23_atomicity() -> Ledger:
    # V23：一组操作全部成功或全部失败。扣库存后建订单失败，rollback 必须还原。
    ledger = Ledger(stock=10)
    before = ledger.snapshot()
    try:
        ledger.stock -= 2
        raise RuntimeError("create order failed")
    except RuntimeError:
        ledger.stock, ledger.order_created = before
    assert ledger.stock == 10
    assert ledger.order_created is False
    print("实际结果总结：V23 rollback 后 stock 仍是 10，订单未创建。")
    return ledger


def demo_v24_lost_update() -> int:
    # V24：两个事务都按自己读到的旧值回写，后提交者覆盖先提交者，合计少扣一次。
    committed = 10
    a_seen = committed
    b_seen = committed
    committed = a_seen - 1
    committed = b_seen - 1
    assert committed == 9
    assert committed != 8
    print("实际结果总结：V24 Lost Update 后库存是 9，不是两人各扣 1 后的 8。")
    return committed


def demo_v26_visibility() -> None:
    # V26：B 已经 commit 之后，A 该不该看见新值，取决于隔离/快照，而不是会不会少扣。
    committed = 10
    snapshot_a = committed
    committed = 9
    read_committed_second = committed
    snapshot_second = snapshot_a
    assert read_committed_second == 9
    assert snapshot_second == 10
    print("实际结果总结：V26 RC 第二次读到 9；snapshot 仍读到 10。")


def demo_problems_and_tools() -> None:
    demo_v23_atomicity()
    demo_v24_lost_update()
    demo_v26_visibility()


def main() -> None:
    demo_problems_and_tools()


if __name__ == "__main__":
    main()
    print("--- v26 transaction_timeline_demo 运行完毕 ---")
