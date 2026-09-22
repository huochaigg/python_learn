from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class AgentContext:
    # Local Context：Python 应用内部依赖，通过 Runner.run(context=...) 传给 Tool。
    # 它不会自动变成 LLM prompt。只有 Tool 返回值才会进入模型上下文。
    db: AsyncSession
    user_id: int | None = None
