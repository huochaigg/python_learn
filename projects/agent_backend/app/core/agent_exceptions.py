"""应用层 Agent 错误。这些 code 不是 SDK 提供的，是本项目自己映射出来的。"""

from __future__ import annotations

from agents.exceptions import (
    AgentsException,
    InputGuardrailTripwireTriggered,
    MaxTurnsExceeded,
    ModelBehaviorError,
    ModelTimeoutError,
    OutputGuardrailTripwireTriggered,
    ToolTimeoutError,
)
from agents.exceptions import (
    ToolInputGuardrailTripwireTriggered,
    ToolOutputGuardrailTripwireTriggered,
)


INPUT_GUARDRAIL_BLOCKED = "INPUT_GUARDRAIL_BLOCKED"
OUTPUT_GUARDRAIL_BLOCKED = "OUTPUT_GUARDRAIL_BLOCKED"
AGENT_MAX_TURNS = "AGENT_MAX_TURNS"
AGENT_MODEL_ERROR = "AGENT_MODEL_ERROR"
AGENT_TIMEOUT = "AGENT_TIMEOUT"
AGENT_TOOL_ERROR = "AGENT_TOOL_ERROR"
AGENT_RUN_FAILED = "AGENT_RUN_FAILED"

_PUBLIC_MESSAGES = {
    INPUT_GUARDRAIL_BLOCKED: "当前问题不在供应链助手范围内",
    OUTPUT_GUARDRAIL_BLOCKED: "输出未通过安全检查，已拦截",
    AGENT_MAX_TURNS: "处理轮次过多，请简化问题后重试",
    AGENT_MODEL_ERROR: "模型输出无法处理，请重试",
    AGENT_TIMEOUT: "处理超时，请稍后重试",
    AGENT_TOOL_ERROR: "工具调用被安全策略拦截",
    AGENT_RUN_FAILED: "助手暂时无法处理该请求",
}


class AgentRunError(Exception):
    # 是什么：Service 识别 SDK 异常后抛出的统一业务异常。
    # 为什么用：Router 不再堆叠一长串 except；HTTP 只暴露 code + 安全文案。
    # 什么时候：Runner.run / run_streamed 失败，或 Guardrail tripwire。
    # 参数：code 应用层错误码；message 给前端的短句；status_code HTTP 状态。
    # 返回值：由 FastAPI exception handler 转成 JSON。
    # 副作用：无。不要把 str(原始 SDK 异常) 发给前端。
    # 常见坑：INPUT_GUARDRAIL_BLOCKED 不是 SDK 字段；SDK 只有 InputGuardrailTripwireTriggered。
    # 对应：NestJS Filter 把领域异常映射成 HTTP；不是 LangChain 自动错误码。

    def __init__(self, code: str, message: str, status_code: int = 500) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def public_message_for(code: str) -> str:
    return _PUBLIC_MESSAGES.get(code, _PUBLIC_MESSAGES[AGENT_RUN_FAILED])


def is_guardrail_block(code: str) -> bool:
    return code in {INPUT_GUARDRAIL_BLOCKED, OUTPUT_GUARDRAIL_BLOCKED}


def map_sdk_exception(exc: BaseException) -> AgentRunError:
    if isinstance(exc, AgentRunError):
        return exc
    if isinstance(exc, InputGuardrailTripwireTriggered):
        return AgentRunError(INPUT_GUARDRAIL_BLOCKED, public_message_for(INPUT_GUARDRAIL_BLOCKED), 400)
    if isinstance(exc, OutputGuardrailTripwireTriggered):
        return AgentRunError(OUTPUT_GUARDRAIL_BLOCKED, public_message_for(OUTPUT_GUARDRAIL_BLOCKED), 400)
    if isinstance(exc, (ToolInputGuardrailTripwireTriggered, ToolOutputGuardrailTripwireTriggered)):
        return AgentRunError(AGENT_TOOL_ERROR, public_message_for(AGENT_TOOL_ERROR), 400)
    if isinstance(exc, MaxTurnsExceeded):
        return AgentRunError(AGENT_MAX_TURNS, public_message_for(AGENT_MAX_TURNS), 502)
    if isinstance(exc, ModelBehaviorError):
        return AgentRunError(AGENT_MODEL_ERROR, public_message_for(AGENT_MODEL_ERROR), 502)
    if isinstance(exc, (ModelTimeoutError, ToolTimeoutError)):
        return AgentRunError(AGENT_TIMEOUT, public_message_for(AGENT_TIMEOUT), 504)
    if isinstance(exc, AgentsException):
        return AgentRunError(AGENT_RUN_FAILED, public_message_for(AGENT_RUN_FAILED), 500)
    return AgentRunError(AGENT_RUN_FAILED, public_message_for(AGENT_RUN_FAILED), 500)


def error_payload(error: AgentRunError) -> dict[str, str]:
    return {"code": error.code, "message": error.message}
