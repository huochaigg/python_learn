"""V20 速查：SQLAlchemy 2.x 核心关系。

运行：uv run python lessons/v20/notes.py
"""

NOTES = """
Engine
  连库入口：URL、方言/驱动、连接池。不等于某一条 Connection。

Connection
  真正拿去执行 SQL 的连接。通常由 Engine 在需要时借出。

DeclarativeBase
  ORM 声明式基类。User(Base) 进入同一套 mapping/metadata。

Mapped / mapped_column
  Mapped[T]：这是 ORM 映射属性 + 类型信息。
  mapped_column()：主键、唯一、索引、可空、默认值等列配置。
  Mapped[str] 偏向非空；Mapped[str | None] 允许 None。

metadata / create_all
  metadata 收集已加载 Model 的表。
  create_all 建还不存在的表。不是 Alembic，不能当 Prisma migrate。

sessionmaker
  Session 工厂。SessionLocal() 才是新 Session。不要全局共用一个 Session。

Session
  ORM 工作单元：查询、持久化、事务、Identity Map。
  需要时才从 Engine 取连接。Session != Connection。

add / flush / commit / refresh / rollback
  add：纳入 Session 管理，不是已经插入成功。
  flush：把变更发给数据库，事务未最终提交。
  commit：提交事务。
  rollback：撤销当前事务。
  refresh：再从库读对象最新字段。不是每次必须。

select / execute / scalars / where / get
  select(User) 现代查询，不要优先 session.query。
  execute 得到 Result。
  scalars().all() 抽出 ORM 对象列表。
  where 拼 WHERE。
  get(Model, pk) 主键查询，像 findUnique({id})。
  scalar_one_or_none：0→None，1→对象，多条报错。

delete
  标记删除，commit/flush 才真正 DELETE。

请求链
  FastAPI → Depends(get_db) → Session → Service → ORM → commit/query
  → ORM Object → Pydantic Response（from_attributes=True）
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v20 notes 运行完毕 ---")
