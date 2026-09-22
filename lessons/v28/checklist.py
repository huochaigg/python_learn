"""
文件作用：V28 自测题。只问不答。
运行命令：uv run python lessons/v28/checklist.py
观察重点：先判断哪个调用要 await，再对照 notes。
"""

QUESTIONS = [
    "1. create_async_engine 和 create_engine 的角色有何相同、有何不同？",
    "2. 为什么同步 PyMySQL 不能直接给 AsyncEngine 用？",
    "3. 为什么不要每个 HTTP Request 都 create_async_engine？",
    "4. async_sessionmaker 是 Session 还是 factory？",
    "5. 当前项目为什么设置 expire_on_commit=False？这是异步硬性规定吗？",
    "6. 为什么同一个 AsyncSession 不能给多个 asyncio Task 共用？",
    "7. select(User) 要不要 await？await session.execute(stmt) 呢？",
    "8. session.add(user) 为什么不 await？commit/refresh 为什么要 await？",
    "9. await session.get(User, id) 和 session.get 同步版差在哪？",
    "10. 为什么 create_all 要写成 conn.run_sync(Base.metadata.create_all)？",
    "11. async with session.begin() 和 V23 事务语义有什么没变？",
    "12. IntegrityError 之后为什么必须 await session.rollback()？",
    "13. 为什么 Async ORM 更要避免 relationship lazy loading？",
    "14. OrderResponse 含 items 时，为什么必须提前 selectinload？",
    "15. 为什么不要每个请求 await engine.dispose()？",
]


def main() -> None:
    print("===== V28 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v28 checklist 运行完毕 ---")
