from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AgentContext:
    # Local Context：本次 Agent Run 的本地依赖（Tool 查库存用的 AsyncSession）。
    # 它不是 Conversation History。历史由 SDK Session 按 session_id 加载。
    db: AsyncSession
    user_id: int | None = None
