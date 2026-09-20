"""V24 速查：并发更新。

运行：uv run python lessons/v24/notes.py
"""

NOTES = """
Lost Update
  两个事务都读到 10，都按 10 去减，后写覆盖先写。最终像只卖出 1 件。
  事务保证的是「一个事务内部原子」，挡不住这种并发读写。

Pessimistic Lock / FOR UPDATE
  with_for_update() 在支持的库上生成 SELECT ... FOR UPDATE。
  锁行直到本事务 commit/rollback。锁的是数据库，不是 Python Lock。
  事务必须短，不要持锁做外部 IO。SQLite 不能当真实行锁实验。

nowait / skip_locked
  nowait：拿不到锁尝试立即失败。
  skip_locked：跳过已被锁住的行，多 Worker 抢任务更常见。
  各库支持不同，不要当正式库存默认逻辑。

Optimistic Lock / version_id_col
  读 version=N，更新要求仍是 N，成功后版本增加。
  __mapper_args__ version_id_col 让 ORM flush 的 UPDATE/DELETE 带上版本条件。
  只作用于 ORM 对象 flush，不自动套到 bulk update()。

StaleDataError
  ORM 以为能更新某行，版本等条件没命中。先 rollback，再当并发冲突处理。

Atomic UPDATE / rowcount
  UPDATE stock SET quantity=quantity-need WHERE sku=? AND quantity>=need
  判断和扣减同一条 SQL，没有「先 SELECT 再 UPDATE」窗口。
  单条 UPDATE 的 rowcount 1=成功，0=没匹配（无 sku 或库存不够，语义不同）。
  多 SKU 仍要放进同一个 Transaction，一个失败全部 rollback。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v24 notes 运行完毕 ---")
