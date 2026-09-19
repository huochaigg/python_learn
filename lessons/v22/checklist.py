"""V22 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v22/checklist.py
"""

QUESTIONS = [
    "1. ForeignKey 和 relationship() 是同一回事吗？各自属于哪一层？",
    "2. orders 表里有没有 items 列？那为什么还能写 order.items？",
    "3. ForeignKey 为什么通常放在 OrderItem.order_id，而不是 Order 上？",
    "4. Order.items 和 OrderItem.order 分别是一对多还是多对一？类型有何不同？",
    "5. back_populates 在做什么？为什么 SQLAlchemy 2.x 不把 backref 当主写法？",
    "6. item.order = order 之后，order.items 里为什么会出现这个 item？",
    "7. 访问尚未加载的 order.items 为什么可能再发一条 SQL？这叫什么？",
    "8. N+1 是怎么产生的？为什么说它不是 SQLAlchemy 特有问题？",
    "9. 列表接口如果返回嵌套 items，为什么不要等 Pydantic 序列化时再触发 lazy load？",
    "10. selectinload 通常为什么是两条 SQL？IN (...) 在加载什么？",
    "11. 10 个订单用 selectinload 后，理想观察大概从 11 条 SQL 降到 2 条，这个数字为什么不能写成永远保证？",
    "12. joinedload 为什么可能导致父行在 Result 里重复？这和 collection 基数有什么关系？",
    "13. Result.unique() 是 SQL DISTINCT 吗？什么时候必须 unique()？",
    "14. join() 和 joinedload() 差在哪？为什么不能因为 SQL 都有 JOIN 就混用？",
    "15. 按 sku 过滤订单时，为什么一个订单两条相同 sku 可能让 Order 对象重复出现？",
    "16. many-to-one 的 item.order 也是 relationship 吗？和 list collection 有何不同？",
    "17. 教学对比三种加载策略时，为什么每段最好 new 一个 Session？Identity Map 会怎样干扰？",
    "18. 默认 cascade 大致做什么？为什么不要把 delete-orphan 当成方便的业务默认配置？",
    "19. Prisma include: { items: true } 能帮你理解什么？它和 selectinload 是不是同一个机制？",
    "20. AsyncSession 下，隐式 lazy IO 为什么要更谨慎？",
]


def main() -> None:
    print("===== V22 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v22 checklist 运行完毕 ---")
