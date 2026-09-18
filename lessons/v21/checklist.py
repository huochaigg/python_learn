"""V21 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v21/checklist.py
"""

QUESTIONS = [
    "1. where 里的 User.age >= 18 是立刻算出来的 Python bool 吗？它实际生成什么？",
    "2. 连续 .where(a).where(b) 和 .where(a, b) / .where(*conditions) 通常是什么关系？",
    "3. 简单多个 AND 时，为什么不必强制所有代码都写成 and_()？and_() 更适合什么场景？",
    "4. SQLAlchemy OR 为什么不能写成 User.name.contains(k) or User.email.contains(k)？",
    "5. in_() 生成什么 SQL？它和 Python `value in list` 有何不同？",
    "6. contains(keyword) 和 like / ilike 大致对应什么 SQL 语义？",
    "7. 动态筛选为什么用 conditions=[] 再 append，而不是每个参数组合写一棵 if/else？",
    "8. Query 参数 active=False 时，为什么不能写 if active: 再加条件？",
    "9. min_age / max_age 为 None 时为什么不要无脑 append User.age >= min_age？",
    "10. order_by()、.asc()、.desc() 分别做什么？默认为什么常加 created_at DESC, id DESC？",
    "11. sort_by 为什么必须白名单映射到 User.id / User.name 这些列，而不能把前端字符串拼进 SQL？",
    "12. offset 如何根据 page 和 page_size 计算？limit 表示什么？",
    "13. 分页查询为什么必须明确 ORDER BY？没有排序时数据库承诺稳定顺序吗？",
    "14. slice(start, stop) 和 offset/limit 是什么关系？主业务分页为什么仍优先显式 offset/limit？",
    "15. total count 为什么要用 func.count() 让数据库做，而不是查出全部 ORM 再 len()？",
    "16. count query 为什么必须复用列表查询同一套 conditions，而且不能带 offset/limit？",
    "17. session.scalar(count_stmt) 适合什么查询？它和 execute().scalars().all() 差在哪？",
    "18. exists() 和 session.get(User, id) 有什么区别？什么时候用 scalar_one_or_none？",
    "19. UserQuery 是 ORM Model 吗？为什么用 Pydantic / Query Dependency 承接筛选参数？",
    "20. offset pagination 适合什么场景？深分页时可能有什么问题？",
]


def main() -> None:
    print("===== V21 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v21 checklist 运行完毕 ---")
