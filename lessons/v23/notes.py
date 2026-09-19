"""V23 速查：事务边界。

运行：uv run python lessons/v23/notes.py
"""

NOTES = """
Transaction
  多个数据库操作组成一个原子工作单元。
  全部成功 commit；任意步骤失败 rollback。用来消灭「部分成功」。

autobegin
  默认 Session 第一次真正碰数据库时，通常会自动进入事务。
  没写 begin() 也不等于「没有事务」。本课不改 autobegin=False。

commit
  先 flush pending changes，再最终提交事务（拍板）。
  已经 commit 的内容，后面的 rollback 撤不回去。

rollback
  撤销当前尚未提交事务中的修改。
  不会撤销之前已经 commit 的事务。失败后应 rollback 再 raise。

flush
  把 Session pending changes 发到数据库（SQL 可能已经执行），事务还没拍板。
  不是小型 commit。后面 rollback 仍可撤销。
  拿 order.id / 提前撞约束时用 flush，不要为了拿主键就 commit。
  flush 失败后 Session 事务进入失败状态，必须 rollback 或关掉 Session。

Session.begin()
  显式划定事务范围。with 正常退出 commit，异常退出 rollback 并继续传播。
  对照 V6：进入 with = 进入事务；正常退出提交；异常退出回滚。

transaction boundary
  「创建订单 + 明细 + 扣库存」是一个业务动作，共享一个事务。
  内部 _check/_create/_deduct 参与外层事务，自己不 commit。
  谁负责 commit：完整用例方法。不要让小工具函数到处 commit。

Session scope vs Transaction scope
  一个 FastAPI 请求通常 Depends 一个 Session（ORM 工作环境）。
  Transaction 是其中一批必须一起成功/失败的数据库操作。
  Session 生命周期不等于 Transaction 生命周期。

Atomicity
  失败：库存不变，不能残留半条 Order/OrderItem。
  成功：Order、OrderItem、Stock 扣减一起生效。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v23 notes 运行完毕 ---")
