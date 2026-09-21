"""
文件作用：V25 自测题。只问不答。
重点概念：UNIQUE 兜底、三层校验、IntegrityError、幂等 Key。
观察重点：先自己写答案，再对照 notes / demo。
"""

QUESTIONS = [
    "1. 为什么 email_exists() 之后仍然需要数据库 UNIQUE？",
    "2. NOT NULL 和 Pydantic required 是一回事吗？分别拦哪一层？",
    "3. IntegrityError 可能来自哪些约束？",
    "4. IntegrityError 后为什么必须 rollback？不 rollback 再查询会怎样？",
    "5. 为什么不要把 str(IntegrityError) 直接返回给前端？",
    "6. CheckConstraint 的 name 有什么用？",
    "7. SQLite 为什么要 PRAGMA foreign_keys=ON？MySQL 也要写吗？",
    "8. 幂等是什么意思？是禁止重复发请求，还是禁止重复副作用？",
    "9. 同一个 Idempotency-Key 为什么需要 UNIQUE？",
    "10. 两个不同 Idempotency-Key 能否创建两个订单？这说明幂等限制的是什么？",
    "11. 为什么服务端不要自动生成随机 Idempotency-Key？",
    "12. POST 默认是幂等的吗？",
    "13. A/B 都先查到 key 不存在，两个 INSERT 撞 UNIQUE 之后正确做法是什么？",
    "14. Pydantic 校验、Service 校验、数据库约束各解决什么问题？",
    "15. 已经有 Pydantic/Service 校验，为什么还不能删掉数据库约束？",
    "16. DuplicateEmailError 和 IntegrityError 谁应该出现在 HTTP JSON 里？",
    "17. 先查再插的并发窗口，和 V24 先 SELECT 再 UPDATE 的窗口有什么相似处？",
    "18. event.listens_for(engine, connect) 在本课解决的是哪件 SQLite 特例？",
]


def main() -> None:
    print("===== V25 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v25 checklist 运行完毕 ---")
