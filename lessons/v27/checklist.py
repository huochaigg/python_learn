"""
文件作用：V27 自测题。只问不答。
运行命令：uv run python lessons/v27/checklist.py
观察重点：先自己画执行链和配置链，再对照 notes。
"""

QUESTIONS = [
    "1. 为什么不要每个 HTTP Request 都 create_engine？",
    "2. mysql+pymysql 里 mysql 和 pymysql 各是什么角色？",
    "3. 为什么用 URL.create() 而不是手写 f-string URL？",
    "4. BaseSettings 和普通 BaseModel 的使用目标有什么不同？",
    "5. pool_size=5 是否表示整个系统永远只有 5 个数据库连接？多 worker 时会怎样？",
    "6. max_overflow 是数据库最大连接数吗？",
    "7. pool_timeout 超时通常代表什么？",
    "8. pool_pre_ping 会在每条 SQL 前 ping 吗？它主要解决什么？",
    "9. pool_recycle 是每 N 秒重启整个连接池吗？",
    "10. Session.close() 会永久断开 MySQL TCP 吗？",
    "11. Session 和 Connection 是同一个东西吗？",
    "12. GET /health 和 GET /health/db 分别证明什么？",
    "13. 为什么健康检查不能返回 DATABASE_URL 或密码？",
    "14. create_all 是 Migration 吗？后面应该用什么？",
    "15. 连接失败时为什么不能悄悄改成 SQLite？",
]


def main() -> None:
    print("===== V27 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v27 checklist 运行完毕 ---")
