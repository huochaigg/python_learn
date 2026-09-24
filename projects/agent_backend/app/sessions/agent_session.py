"""SDK Session 工厂。SQLAlchemySession ≠ 业务 AsyncSession。"""

from sqlalchemy import text

from agents.extensions.memory import SQLAlchemySession

from ..core.database import engine

_SDK_TABLE_DDL = (
    """
    CREATE TABLE IF NOT EXISTS agent_sessions (
        session_id VARCHAR(128) NOT NULL PRIMARY KEY,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS agent_messages (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        session_id VARCHAR(128) NOT NULL,
        message_data TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_agent_messages_session_time (session_id, created_at),
        CONSTRAINT fk_agent_messages_session
            FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
)


def get_agent_session(session_id: str) -> SQLAlchemySession:
    # SQLAlchemySession：SDK 的历史持久化实现。
    # 是什么：按 session_id 读写模型对话条目（user/assistant/tool item）。
    # 为什么用：让 Runner 跨 HTTP 请求自动加载/保存历史，不必自己拼接 messages。
    # 什么时候：每次 Runner.run / run_streamed 之前按 conversation_id 构造。
    # 参数：session_id 会话标识；engine 复用 V30 的 mysql+asyncmy AsyncEngine。
    # 返回：新的 SQLAlchemySession 对象。对象本身可以丢弃，历史在 MySQL。
    # 副作用：读写 agent_sessions / agent_messages；自己开事务，不与 Tool 的 AsyncSession 共享。
    # 常见坑：官方 create_tables=True 在 MySQL 上因 VARCHAR 无长度失败，所以建表用兼容 DDL。
    return SQLAlchemySession(
        session_id,
        engine=engine,
        create_tables=False,
        ensure_ascii=False,
    )


async def init_sdk_session_tables() -> None:
    async with engine.begin() as connection:
        rows = await connection.execute(
            text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = DATABASE() "
                "AND table_name IN ('agent_sessions', 'agent_messages')"
            )
        )
        have = {str(row[0]).lower() for row in rows.all()}
        if "agent_sessions" not in have:
            await connection.execute(text(_SDK_TABLE_DDL[0]))
        if "agent_messages" not in have:
            await connection.execute(text(_SDK_TABLE_DDL[1]))
