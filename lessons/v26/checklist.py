"""
文件作用：V26 自测题。只问不答。
运行命令：uv run python lessons/v26/checklist.py
重点概念：脏读、不可重复读、幻读、隔离级别、MVCC、死锁。
观察重点：先自己画 A/B 时间线再对照 notes。
"""

QUESTIONS = [
    "1. Isolation Level 定义的是什么？它等于某一种锁吗？",
    "2. Dirty Read 读到了什么？对方 rollback 之后意味着什么？",
    "3. READ COMMITTED 主要想解决哪种并发现象？",
    "4. 不可重复读和幻读差在哪？一个改的是行值还是行集合？",
    "5. 为什么不要把某个数据库的默认隔离行为当成 SQL 标准本身？",
    "6. MVCC 是 SQLAlchemy version_id_col 吗？和 V24 乐观锁字段是一回事吗？",
    "7. MVCC 是否等于「完全没有锁」？",
    "8. 为什么 SERIALIZABLE 成本通常更高？",
    "9. isolation_level 必须在什么时候设置？事务进行中途能随便改吗？",
    "10. get_isolation_level() 的返回值能假定所有数据库都一样吗？",
    "11. AUTOCOMMIT 是第五种标准隔离级别吗？它实际改的是什么？",
    "12. Deadlock 怎么形成？数据库通常怎么处理，而不是永远卡住？",
    "13. 统一按 SKU 排序再加锁，为什么能降低死锁风险？为什么不能说绝对不会死锁？",
    "14. 死锁或事务中断后，为什么要 rollback 并从起点重试完整 transaction？",
    "15. V23 事务、V24 并发更新、V26 隔离级别各解决什么问题？",
    "16. 事务 A 两次读同一行，中间 B 已 commit 修改，A 第二次看到新值，这叫什么？",
    "17. 事务 A 两次 count(age>=18)，中间 B 插入符合条件的新行，这叫什么？",
    "18. 为什么本课很多 Demo 是时间线模拟，而不是声称 SQLite 完整复现了 MySQL 行为？",
    "19. 读到别人未提交的库存 0，但对方随后 rollback，业务上可能出什么错？",
    "20. 提高隔离级别能不能代替 V24 的原子 UPDATE / 乐观锁？",
]


def main() -> None:
    print("===== V26 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v26 checklist 运行完毕 ---")
