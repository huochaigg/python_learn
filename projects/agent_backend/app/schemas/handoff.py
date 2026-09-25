from pydantic import BaseModel, Field


class HandoffData(BaseModel):
    # input_type：交接 Tool 的参数 Schema。模型生成 JSON，SDK 用 Pydantic 校验。
    # 它不是下一位 Agent 的用户输入，也不能替代 AgentContext 里的 user_id / db。
    reason: str = Field(min_length=1, description="为什么把当前问题交给这个专家")


class MultiAgentChatResponse(BaseModel):
    # HTTP DTO。约束接口 JSON，不约束 Triage/专家的 output_type，避免和 V32 的 response_model 混用。
    conversation_id: str
    answer: str
    last_agent: str
    handoffs: list[str]
    reasons: list[str] = Field(default_factory=list)
