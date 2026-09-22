"""
文件作用：用 list/filter 执行范围查询，对比 RC 与 snapshot 下幻读是否发生。
运行命令：uv run python lessons/v26/phantom_read_demo.py
重点概念：Phantom Read、范围查询 age>=18、结果集增减。
观察重点：RC 下 count 从 2 变成 3；snapshot 下仍是 2。这是可执行概念模型，不是 SQLite 内核隔离实验。
"""

from copy import deepcopy


def query_adults(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in rows if int(row["age"]) >= 18]


def demo_phantom_read() -> None:
    # Phantom Read：相同条件的行集合变了。和「已有行字段值变化」不是同一件事。
    committed: list[dict[str, object]] = [
        {"name": "Ada", "age": 18},
        {"name": "Tom", "age": 20},
    ]

    first_rc = query_adults(committed)
    snapshot = deepcopy(committed)

    committed.append({"name": "Bob", "age": 20})
    second_rc = query_adults(committed)
    second_snapshot = query_adults(snapshot)

    assert len(first_rc) == 2
    assert len(second_rc) == 3
    assert len(second_snapshot) == 2
    print(
        "实际结果总结："
        f"READ COMMITTED 模拟 count {len(first_rc)}→{len(second_rc)}，发生幻读；"
        f"snapshot 仍是 {len(second_snapshot)}。"
    )


def main() -> None:
    demo_phantom_read()


if __name__ == "__main__":
    main()
    print("--- v26 phantom_read_demo 运行完毕 ---")
