"""
文件作用：V25 速查。约束、IntegrityError、幂等各记几行。
重点概念：Application Validation、Database Constraint、UNIQUE、NOT NULL、CHECK、FK、rollback、Idempotency。
观察重点：应用层是提前发现，数据库约束是最终兜底。
"""

NOTES = """
Application Validation
  Pydantic/FastAPI：请求格式。Service：业务规则和友好错误。
  先查 email/key 改善体验，不能当成并发安全。

Database Constraint
  数据库最后一道完整性防线。有了应用校验也不该拆掉 UNIQUE/NOT NULL/CHECK/FK。

UNIQUE
  列值唯一。并发两个 insert，数据库只放过一个。

NOT NULL
  列不能是 NULL。和 Pydantic required 不是同一层。

CHECK
  数据库检查表达式，例如 quantity >= 0。命名约束方便定位。

ForeignKey
  子行必须指向存在的父行。SQLite 默认不强制，需要 PRAGMA foreign_keys=ON。

IntegrityError
  约束失败信号，不是业务文案。flush/commit 失败后 rollback，再转业务异常。

rollback
  失败 Session 必须先恢复事务，才能继续用。关联 V23。

Idempotency
  同一业务请求重复执行，不要产生重复副作用。
  不是禁止同一用户下多单；不同 Idempotency-Key 可以创建多个订单。
  同一个 key 必须 UNIQUE。先查仍有窗口，冲突后按 key 再读已有结果。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
    print("--- v25 notes 运行完毕 ---")
