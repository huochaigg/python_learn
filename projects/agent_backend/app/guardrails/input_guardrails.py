from __future__ import annotations

import re

from pydantic import BaseModel
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, input_guardrail

from ..agents.context import AgentContext

# 确定性关键词。不是 LLM 分类器，不能当权限系统。
_ALLOW_MARKERS = (
    "sku",
    "库存",
    "订单",
    "商品",
    "供应链",
    "stock",
    "order",
    "product",
)
_BLOCK_MARKERS = (
    "数学题",
    "解方程",
    "证明题",
    "math problem",
    "solve this equation",
    "写一首诗",
)


class ScopeCheckResult(BaseModel):
    in_scope: bool
    reason: str


def extract_user_text(agent_input: str | list[object]) -> str:
    if isinstance(agent_input, str):
        return agent_input
    parts: list[str] = []
    for item in agent_input:
        if isinstance(item, str):
            parts.append(item)
            continue
        if isinstance(item, dict):
            content = item.get("content")
            if isinstance(content, str):
                parts.append(content)
    return "\n".join(parts)


def classify_business_scope(text: str) -> ScopeCheckResult:
    lowered = text.strip().lower()
    if not lowered:
        return ScopeCheckResult(in_scope=False, reason="empty")
    if any(marker in lowered for marker in _BLOCK_MARKERS):
        return ScopeCheckResult(in_scope=False, reason="off_topic")
    if re.search(r"sku\d+|ord\d+", lowered):
        return ScopeCheckResult(in_scope=True, reason="business_id")
    if any(marker in lowered for marker in _ALLOW_MARKERS):
        return ScopeCheckResult(in_scope=True, reason="business")
    return ScopeCheckResult(in_scope=False, reason="unknown_topic")


def evaluate_business_scope(
    ctx: RunContextWrapper[AgentContext],
    agent: Agent[AgentContext],
    agent_input: str | list[object],
) -> GuardrailFunctionOutput:
    # @input_guardrail：把函数变成 InputGuardrail，挂到第一个 Agent。
    # 是什么：运行前的输入检查。tripwire_triggered=True 会抛 InputGuardrailTripwireTriggered。
    # 为什么用：挡住明显非业务问题，避免无意义消耗模型和 Tool。
    # 什么时候：run_in_parallel=False 时在 Agent 开始前阻塞执行；True 则与 Agent 并行。
    # 参数：ctx 本轮 Context；agent 当前 Agent；agent_input 用户输入或消息列表。
    # 返回值：GuardrailFunctionOutput。output_info 是检查细节，不是 Agent 最终回答。
    # 副作用：触发后中断 Runner。False 时不改输入，Agent 继续。
    # 常见坑：默认并行时 Agent/Tool 可能已经开始；敏感操作必须阻塞。不是普通 Tool。
    # 对应：NestJS Guards / interceptor；不是 LangChain Tool。
    _ = ctx
    _ = agent
    result = classify_business_scope(extract_user_text(agent_input))
    return GuardrailFunctionOutput(
        output_info=result.model_dump(),
        tripwire_triggered=not result.in_scope,
    )


check_business_scope = input_guardrail(name="business_scope", run_in_parallel=False)(
    evaluate_business_scope
)
