"""
文件作用：V26 速查。隔离级别、三种并发现象、MVCC、Deadlock 各记几行。
运行命令：uv run python lessons/v26/notes.py
重点概念：READ UNCOMMITTED / COMMITTED / REPEATABLE READ / SERIALIZABLE、Dirty Read、不可重复读、幻读、MVCC、Deadlock。
观察重点：会画 A/B 时间线，判断 B 改完之后 A 该不该看见。
"""

NOTES = """
READ UNCOMMITTED
  最弱。可能脏读。很少当业务默认。

READ COMMITTED
  只看见已提交数据，挡住脏读。同一行两次读仍可能不同。

REPEATABLE READ
  希望同一事务内同一行稳定。幻读是否出现看数据库实现，不要只背标准表。

SERIALIZABLE
  并发现象最少，代价通常更高。具体实现各库不同。

Dirty Read
  看见别人还没提交的数据。对方 rollback 后，刚才读到的是无效中间状态。

Non-repeatable Read
  同一行前后两次读到不同字段值。不是集合多了一行。

Phantom Read
  同一个范围查询，结果行集合变了（多出行/少了行）。

MVCC
  数据库用多版本/快照控制可见性，提高读写并发。
  MVCC != version_id_col；也不等于完全没有锁。

Deadlock
  循环等待。库常中止其中一个事务。
  失败方 rollback，必要时从起点重试完整 transaction，不要从中间 SQL 接着跑。
  统一加锁顺序只能降低概率，不是绝对不会死锁。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v26 notes 运行完毕 ---")
