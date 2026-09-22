"""
文件作用：V26 概念定位索引。运行时校验函数名存在，避免索引和真实 Demo 脱节。
运行命令：uv run python lessons/v26/concept_index.py
重点概念：隔离级别、Dirty Read、Non-repeatable Read、Phantom Read、MVCC、isolation_level、Deadlock。
观察重点：回头查概念时先看这里，再打开对应可执行 Demo 函数。
"""

import deadlock_demo
import dirty_read_demo
import isolation_level_demo
import isolation_overview_demo
import mvcc_demo
import non_repeatable_read_demo
import phantom_read_demo
import transaction_timeline_demo

CONCEPT_INDEX = {
    "Isolation Level": (isolation_overview_demo, "demo_isolation_matrix"),
    "Dirty Read": (dirty_read_demo, "demo_dirty_read"),
    "Non-repeatable Read": (non_repeatable_read_demo, "demo_read_committed_non_repeatable_read"),
    "Non-repeatable Read (snapshot)": (non_repeatable_read_demo, "demo_repeatable_snapshot"),
    "Phantom Read": (phantom_read_demo, "demo_phantom_read"),
    "MVCC": (mvcc_demo, "demo_mvcc_snapshot_visibility"),
    "Deadlock": (deadlock_demo, "demo_circular_wait"),
    "consistent lock order": (deadlock_demo, "demo_consistent_lock_order"),
    "SQLAlchemy isolation_level API": (isolation_level_demo, "demo_get_and_change_isolation_level"),
    "V23 原子性": (transaction_timeline_demo, "demo_v23_atomicity"),
    "V24 Lost Update": (transaction_timeline_demo, "demo_v24_lost_update"),
    "V26 可见性": (transaction_timeline_demo, "demo_v26_visibility"),
}


def main() -> None:
    print("===== V26 concept_index =====")
    for name, (module, func_name) in CONCEPT_INDEX.items():
        func = getattr(module, func_name, None)
        assert callable(func), f"{module.__name__} 缺少 {func_name}()"
        print(f"{name} → {module.__name__}.py → {func_name}()")


if __name__ == "__main__":
    main()
    print("--- v26 concept_index 运行完毕 ---")
