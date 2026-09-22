"""
文件作用：V28 速查。AsyncEngine、AsyncSession、await 原则、并发、relationship。
运行命令：uv run python lessons/v28/notes.py
观察重点：能画出 async endpoint → AsyncSession → await execute → AsyncEngine → asyncmy → MySQL。
"""

NOTES = """
async def endpoint → Depends(get_db) → AsyncSession → await execute/commit
→ AsyncEngine → asyncmy → MySQL

select()/where()/order_by() 只是写 SQL 计划，不 await。
execute()/commit()/flush()/refresh()/rollback()/get() 会访问数据库，要 await。
session.add() 只改 Session 状态，不 await。

同一个 AsyncSession 不应通过 asyncio.gather() 同时给多个 Task 使用。
需要并发 DB Task 时通常各自使用独立 AsyncSession（Session per Task）。
这会改变事务边界和连接占用，需要谨慎；不是鼓励把所有 SQL 都 gather。

需要 relationship 时优先 selectinload，不要等 Pydantic 序列化时才查库。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
