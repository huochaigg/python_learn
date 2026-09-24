"""
文件作用：V31 速查。SDK Session、SQLAlchemySession、业务 Conversation/Message、三种 Session 区别。
运行命令：uv run python lessons/v31/notes.py
观察重点：能画出 conversation_id → SQLAlchemySession → Runner → 业务 Message。
"""

from agents.extensions.memory import SQLAlchemySession

from app.core.database import engine

_example = SQLAlchemySession("notes-example", engine=engine, create_tables=False)

NOTES = """
SDK Session
  按 session_id 存模型对话上下文。Runner.run(session=...) 自动 get_items / add_items。
  类似 NestJS 里给 Agent 配的 history store，不是 Prisma Client。

SQLiteSession
  官方 SQLite 实现。默认 :memory:。文件 db_path 才能用同一个库换 session_id 做隔离。

SQLAlchemySession
  官方 SQL 实现。本版复用 mysql+asyncmy AsyncEngine。
  自己开事务写 agent_sessions / agent_messages，不与业务 AsyncSession 共享事务。

session_id
  会话标识。本版 session_id = conversation_id。
  不等于 user_id。一个用户可以有多个 Conversation。

get_items / add_items / pop_item / clear_session
  读历史、追加、弹出最新、清空。
  一次对话不等于两条 Item，可能含 Tool Call / Tool Output。

三种对象
  Agent Session：模型历史。
  SQLAlchemy AsyncSession：数据库工作单元，类似 Prisma 一次交互的事务边界。
  AgentContext：本次 Run 的本地依赖（Tool 的 db），不是聊天记录。

Conversation / Message
  业务表。类似 Prisma Conversation / Message。
  给前端展示、查询、删除。
  SDK 历史给模型继续推理。两套数据不等价，也不自动原子化。

多轮对话
  模型不会天然记住上一次 HTTP。
  同一 conversation_id → 同一 SDK Session → 读出旧历史再跑。

流式保存
  用户消息先写。助手先 pending。
  内存攒完整回答，结束后 completed。
  取消/失败标 failed，不能标 completed。
  不要每个 delta commit。

并发
  同会话两个 Run 可能读到同一份旧历史。
  本版同进程拒绝第二个活动请求（409）。
  asyncio.Lock 不能跨 Worker。

删除
  校验归属 → clear_session → 删 Message → 删 Conversation。
  SDK 清成功、业务删失败要报错，不能返回删除成功。
"""


def main() -> None:
    print(f"example_session_id={_example.session_id}")
    print(NOTES)


if __name__ == "__main__":
    main()
