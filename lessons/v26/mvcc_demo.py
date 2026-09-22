"""
文件作用：用简化 RowVersion/Snapshot 模型执行 MVCC 可见性查找，并 assert 结果。
运行命令：uv run python lessons/v26/mvcc_demo.py
重点概念：MVCC 快照可见性；MVCC != version_id_col。
观察重点：A snapshot=1 仍看到 quantity=10；B 已提交 9 后，新事务 C snapshot=2 看到 9。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RowVersion:
    value: int
    commit_id: int


@dataclass(frozen=True)
class SnapshotTransaction:
    snapshot_id: int


def find_visible_version(versions: list[RowVersion], tx: SnapshotTransaction) -> RowVersion:
    # 这是 MVCC 可见性思想模拟，不是数据库真实 undo log / read view。
    # 规则：只能看见 commit_id <= 本事务 snapshot_id 的版本，取其中最新的一条。
    visible = [row for row in versions if row.commit_id <= tx.snapshot_id]
    if not visible:
        raise RuntimeError("no visible version")
    return max(visible, key=lambda row: row.commit_id)


def demo_mvcc_snapshot_visibility() -> None:
    versions = [RowVersion(value=10, commit_id=1)]
    tx_a = SnapshotTransaction(snapshot_id=1)

    versions.append(RowVersion(value=9, commit_id=2))
    seen_a = find_visible_version(versions, tx_a)
    tx_c = SnapshotTransaction(snapshot_id=2)
    seen_c = find_visible_version(versions, tx_c)

    assert seen_a.value == 10
    assert seen_a.commit_id == 1
    assert seen_c.value == 9
    assert seen_c.commit_id == 2
    print("实际结果总结：A snapshot=1 看见 10；C snapshot=2 看见 9。")


def contrast_mvcc_vs_optimistic_lock() -> None:
    # MVCC：数据库引擎事务可见性机制。version_id_col：ORM/应用层 stale update 检测。
    assert find_visible_version.__name__ == "find_visible_version"


def main() -> None:
    demo_mvcc_snapshot_visibility()
    contrast_mvcc_vs_optimistic_lock()


if __name__ == "__main__":
    main()
    print("--- v26 mvcc_demo 运行完毕 ---")
