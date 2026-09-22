"""
文件作用：用可断言的隔离级别矩阵对照 dirty / non-repeatable / phantom。
运行命令：uv run python lessons/v26/isolation_overview_demo.py
重点概念：Isolation Level、READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ、SERIALIZABLE。
观察重点：每个级别大致挡住哪类并发现象；这是标准意图表，不是某个数据库内核的实测结果。
"""

# Isolation Level：约定事务之间「能看见什么」。不是某一把锁的别名。
# True = 该现象在标准意图下仍可能出现；False = 该级别意图挡住它。
ISOLATION_MATRIX: dict[str, dict[str, bool]] = {
    "READ UNCOMMITTED": {
        "dirty_read": True,
        "non_repeatable_read": True,
        "phantom_read": True,
    },
    "READ COMMITTED": {
        "dirty_read": False,
        "non_repeatable_read": True,
        "phantom_read": True,
    },
    "REPEATABLE READ": {
        "dirty_read": False,
        "non_repeatable_read": False,
        "phantom_read": True,
    },
    "SERIALIZABLE": {
        "dirty_read": False,
        "non_repeatable_read": False,
        "phantom_read": False,
    },
}


def demo_isolation_matrix() -> dict[str, dict[str, bool]]:
    levels = ("READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE")
    assert tuple(ISOLATION_MATRIX) == levels
    assert ISOLATION_MATRIX["READ UNCOMMITTED"]["dirty_read"] is True
    assert ISOLATION_MATRIX["READ COMMITTED"]["dirty_read"] is False
    assert ISOLATION_MATRIX["READ COMMITTED"]["non_repeatable_read"] is True
    assert ISOLATION_MATRIX["REPEATABLE READ"]["non_repeatable_read"] is False
    assert ISOLATION_MATRIX["REPEATABLE READ"]["phantom_read"] is True
    assert ISOLATION_MATRIX["SERIALIZABLE"]["phantom_read"] is False

    print("level               dirty  non-repeatable  phantom")
    print("------------------  -----  --------------  -------")
    for level, flags in ISOLATION_MATRIX.items():
        print(
            f"{level:<18}  "
            f"{str(flags['dirty_read']):<5}  "
            f"{str(flags['non_repeatable_read']):<14}  "
            f"{flags['phantom_read']}"
        )
    print("实际结果总结：矩阵已断言 RC 挡脏读但仍可能不可重复读；SERIALIZABLE 三项都挡。")
    print("具体行为依赖数据库实现，不要把 SQLite/MySQL/PostgreSQL 默认行为当成 SQL 标准本身。")
    return ISOLATION_MATRIX


def main() -> None:
    demo_isolation_matrix()


if __name__ == "__main__":
    main()
    print("--- v26 isolation_overview_demo 运行完毕 ---")
