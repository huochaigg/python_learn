import logging

from sqlalchemy.ext.asyncio import AsyncSession

from agents import Runner

from ..agents.context import AgentContext
from ..agents.product_agent import product_agent

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(self, session: AsyncSession, message: str) -> str:
        # 每个请求新建 AgentContext，把 request-scoped AsyncSession 交给本次 Runner.run。
        # product_agent 是模块级配置，可复用；Session 生命周期跟 HTTP Request 绑定。
        # 不要在这里 asyncio.gather 多个任务共享同一个 session。
        context = AgentContext(db=session)
        try:
            result = await Runner.run(product_agent, message, context=context)
        except Exception:
            logger.exception("Runner.run failed")
            raise
        # RunResult.final_output：本次 Agent Loop 的最终输出，不是整个 RunResult。
        return str(result.final_output)


agent_service = AgentService()
