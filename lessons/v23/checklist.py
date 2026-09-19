"""V23 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v23/checklist.py
"""

QUESTIONS = [
    "1. 事务要解决的「部分成功」具体指什么？commit 和 rollback 各自在什么时候发生？",
    "2. 一次 rollback 能把前面已经 commit 的修改撤回去吗？",
    "3. 一个完整业务操作为什么不要在中间随意 commit？bad_transaction_demo 说明了什么？",
    "4. flush 之后还能 rollback 吗？flush 是不是小型 commit？",
    "5. commit 会不会先 flush？简单 CRUD 为什么通常不必手动 flush？",
    "6. 创建订单需要数据库生成的 order.id 时，为什么可以 flush 而不能 commit？",
    "7. with session.begin() 正常退出和异常退出分别会怎样？这和 V6 Context Manager 怎么对应？",
    "8. 默认 autobegin 是什么意思？没写 begin() 的 CRUD 是不是完全没有事务？",
    "9. 为什么库存扣减、创建 Order、创建 OrderItem 必须放在同一个事务里？",
    "10. _deduct_stock() / _create_items() 为什么不应该自己 commit？",
    "11. Session 生命周期等于 Transaction 生命周期吗？FastAPI Depends Session 和 begin() 各管什么？",
    "12. 复杂业务里「谁负责 commit」应该是小工具函数，还是完整业务用例/transaction boundary？",
    "13. 库存不足 raise InsufficientStockError 时，为什么不要在事务内部 catch 后吞掉或 return None？",
    "14. A001 够、B001 不够时，即使程序已经先改了 A001，最终 A001 为什么必须不变、也不能留半条订单？",
    "15. flush 撞上 unique 约束失败后，为什么还要显式 rollback（或关掉 Session）才能继续？",
    "16. except Exception: rollback; return None 有什么问题？rollback 后应该怎样对待异常？",
    "17. Router 为什么不负责手写一整套 commit/rollback？事务边界放在哪一层？",
    "18. add、flush、commit、rollback 四者对「SQL 是否已发」「事务是否已拍板」分别意味着什么？",
]


def main() -> None:
    print("===== V23 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v23 checklist 运行完毕 ---")
