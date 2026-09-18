"""V20 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v20/checklist.py
"""

QUESTIONS = [
    "1. Engine 是 Connection 吗？它主要管什么？",
    "2. Session 是 Connection 吗？它什么时候才会向 Engine 要连接？",
    "3. sessionmaker / SessionLocal 返回的是 Session 还是 Session 工厂？",
    "4. 为什么不要把一个 Session 实例全局共享给所有 HTTP 请求？",
    "5. Mapped[int] 表示什么？和普通 id: int 差在哪？",
    "6. mapped_column() 负责什么？为什么还要写 primary_key/unique/index？",
    "7. Mapped[str] 和 Mapped[str | None] 在 nullability 上怎么理解？",
    "8. create_all() 会做什么？为什么不能代替 Alembic / Prisma migrate？",
    "9. 为什么 create_all 之前必须 import User Model？",
    "10. session.add(user) 是否已经插入成功？",
    "11. flush 和 commit 的区别是什么？rollback 会怎样？",
    "12. refresh 做什么？是不是每次 CRUD 都必须调用？",
    "13. 为什么列表查询经常是 select → execute → scalars → all 这四步？",
    "14. session.get(User, id) 适合什么查询？和 select().where 怎么选？",
    "15. scalar_one_or_none() 在 0 条、1 条、多条时分别怎样？",
    "16. 修改 user.name 再 commit，为什么能变成 UPDATE？和 Prisma update({data}) 有何不同？",
    "17. session.delete(user) 调用当下，数据库行是否已经没了？",
    "18. Pydantic UserResponse 为什么要 ConfigDict(from_attributes=True)？能和 ORM User 合成一个 class 吗？",
    "19. SQLite 为什么常加 connect_args={\"check_same_thread\": False}？MySQL 需要吗？",
    "20. get_db 里 yield session 对应 V18 的哪件事？请求结束后谁 close？",
]


def main() -> None:
    print("===== V20 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v20 checklist 运行完毕 ---")
