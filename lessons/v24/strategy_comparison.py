"""三种并发策略对照。不写 benchmark，不写绝对排名。

运行（项目根目录）：
uv run python -m lessons.v24.strategy_comparison
"""

TABLE = """
strategy              how                              typical fit
--------------------  -------------------------------  --------------------------------
pessimistic lock      lock row, then change            high conflict + complex in-lock logic
                      SELECT ... FOR UPDATE
optimistic lock       update only if version still N   low conflict; retry/fail is ok
                      version_id_col on ORM flush
atomic UPDATE         one SQL: set qty = qty - n       simple stock/balance/counter
                      where qty >= n; check rowcount

pessimistic = 先锁再改。冲突高、锁内还要做复杂判断时可以考虑。
              代价：等待、吞吐下降、以后才学的死锁。
optimistic  = version 检查冲突。冲突少、允许重试/失败时可以考虑。
atomic      = 数据库一次做条件判断和修改。特别适合库存/余额/计数器。

不要写「原子 UPDATE 永远最好」或「悲观锁最安全」。
先问：是不是简单数值条件修改？够的话优先原子 UPDATE。
复杂临界区再考虑悲观锁；编辑类低冲突再考虑乐观锁。
高并发也别一上来就 Redis 分布式锁。
"""


def main() -> None:
    print(TABLE)


if __name__ == "__main__":
    main()
    print("--- v24 strategy_comparison 运行完毕 ---")
