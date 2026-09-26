from __future__ import annotations

from pydantic import BaseModel, ValidationError
from agents import Agent, GuardrailFunctionOutput, RunContextWrapper, output_guardrail

from ..agents.context import AgentContext
from ..schemas.product import ProductAnalysis, ProductStockResult

_LEAK_MARKERS = (
    "INTERNAL_TEST",
    "__debug__",
    "mysql+",
    "password=",
    "BEGIN RSA",
    "Traceback",
)


class OutputCheckResult(BaseModel):
    ok: bool
    reason: str


def inspect_final_output(agent_output: object) -> OutputCheckResult:
    chunks = [str(agent_output)]
    message = getattr(agent_output, "message", None)
    if isinstance(message, str):
        chunks.append(message)
    text = " ".join(chunks)
    if any(marker.lower() in text.lower() for marker in _LEAK_MARKERS):
        return OutputCheckResult(ok=False, reason="internal_leak")
    if isinstance(agent_output, ProductAnalysis):
        if agent_output.stock < 0:
            return OutputCheckResult(ok=False, reason="negative_stock")
        return OutputCheckResult(ok=True, reason="product_analysis")
    if isinstance(agent_output, ProductStockResult):
        if agent_output.data is not None and agent_output.data.stock < 0:
            return OutputCheckResult(ok=False, reason="negative_stock")
        return OutputCheckResult(ok=True, reason="product_stock_result")
    if isinstance(agent_output, dict):
        try:
            parsed = ProductAnalysis.model_validate(agent_output)
        except ValidationError:
            stock = agent_output.get("stock")
            if isinstance(stock, int) and stock < 0:
                return OutputCheckResult(ok=False, reason="negative_stock")
            return OutputCheckResult(ok=False, reason="invalid_structure")
        if parsed.stock < 0:
            return OutputCheckResult(ok=False, reason="negative_stock")
    return OutputCheckResult(ok=True, reason="text")


def evaluate_final_output(
    ctx: RunContextWrapper[AgentContext],
    agent: Agent[AgentContext],
    agent_output: object,
) -> GuardrailFunctionOutput:
    # @output_guardrail：最终输出已经生成后才执行。
    # 是什么：对 final_output 的策略检查。触发后抛 OutputGuardrailTripwireTriggered。
    # 为什么用：拦住负数库存、内部测试标记等不应给用户看的内容。
    # 什么时候：产生最终结果的 Agent 结束后。Handoff 后是专家的最终输出，不是 Triage 的中间话。
    # 参数：agent_output 已生成的最终结果，可能是 str 或 Pydantic 对象。
    # 返回值：GuardrailFunctionOutput。它不是 FastAPI response_model，也不替代 Pydantic schema。
    # 副作用：触发后不要把原始输出返回前端。追不回已经通过 SSE 发出去的 delta。
    # 常见坑：Output Guardrail ≠ output_type ≠ HTTP response_model。
    # 对应：响应序列化前的 policy filter，不是 class-validator DTO。
    _ = ctx
    _ = agent
    result = inspect_final_output(agent_output)
    return GuardrailFunctionOutput(
        output_info=result.model_dump(),
        tripwire_triggered=not result.ok,
    )


check_final_output = output_guardrail(name="final_output_policy")(evaluate_final_output)
