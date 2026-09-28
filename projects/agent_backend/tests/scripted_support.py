from unittest.mock import MagicMock

from agents import Agent
from agents.testing import ScriptedModel

from app.agents.context import AgentContext
from app.agents.product_agent import product_agent


def fake_context(user_id: int = 1) -> AgentContext:
    return AgentContext(db=MagicMock(), user_id=user_id)


def scripted_product_agent(steps) -> tuple[Agent, ScriptedModel]:
    # 克隆业务 Agent，换上 ScriptedModel。不要改模块级 product_agent.model，避免污染别的测试。
    model = ScriptedModel(steps)
    return product_agent.clone(model=model), model
