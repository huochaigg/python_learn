"""V24 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v24/checklist.py
"""

QUESTIONS = [
    "1. 事务为什么不能自动解决两个请求同时扣同一份库存？",
    "2. Lost Update 里两个 Session 都读到 10 再各自 commit，数据库最终为什么可能是 9 而不是 8？",
    "3. FOR UPDATE 锁的是什么？它是 Python threading.Lock 吗？锁什么时候释放？",
    "4. with_for_update() 生成什么 SQL？SQLite Demo 能不能当成 MySQL 行锁已经验证通过？",
    "5. 悲观锁为什么可能降低吞吐？为什么持锁时不能去调外部支付 / sleep(10)？",
    "6. nowait 和 skip_locked 大概什么语义？为什么不适合当库存扣减的默认写法？",
    "7. 乐观锁为什么需要 version？更新成功后 version 会怎样？",
    "8. version_id_col / __mapper_args__ 在什么时候生效？生效在 SELECT 还是 flush 的 UPDATE？",
    "9. 为什么直接 bulk UPDATE 不能自动等价于 version_id_col？",
    "10. StaleDataError 表示什么？捕获后为什么要先 rollback 再转换成业务异常？",
    "11. 原子 UPDATE 为什么能避免「先查再扣」的竞争窗口？",
    "12. values(quantity=Stock.quantity - qty) 是 Python 先算出来的数字，还是发给数据库的 SQL Expression？",
    "13. WHERE 为什么必须同时有 sku 和 quantity >= need？",
    "14. rowcount=0 可能对应哪两种业务语义？rowcount 为什么不能套到所有 SQL？",
    "15. 原子 UPDATE 成功后还要不要 Transaction？多 SKU 里 C 失败时 A/B 为什么也必须回去？",
    "16. 三种方案各适合什么场景？为什么不要写「原子 UPDATE 永远最好」？",
    "17. 先 SELECT 库存再普通 UPDATE，即使包在一个事务里，为什么仍可能超卖？",
    "18. 看到高并发就上 Redis 分布式锁，这一步跳过了什么更简单的数据库方案？",
    "19. Router 为什么不要到处 catch StaleDataError 再手写 JSON？",
    "20. 事务和并发控制的一句话区别是什么？",
]


def main() -> None:
    print("===== V24 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v24 checklist 运行完毕 ---")
