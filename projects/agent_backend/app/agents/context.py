from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AgentContext:
    # Local Context：本次 Agent Run 的本地依赖（Tool 查库用的 AsyncSession）。
    # 它不是 Conversation History。历史由 SDK Session 按 session_id 加载。
    # Handoff 不会自动开关数据库 Session；所有 Agent 共用本轮传入的同一个 context。
    db: AsyncSession
    user_id: int | None = None
    handoff_reasons: list[str] = field(default_factory=list)
    tool_calls: list[str] = field(default_factory=list)
