from __future__ import annotations

import json
import re

from pydantic import BaseModel
from agents.tool_guardrails import (
    ToolGuardrailFunctionOutput,
    ToolInputGuardrailData,
    ToolOutputGuardrailData,
    tool_input_guardrail,
    tool_output_guardrail,
)

SKU_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")
_SECRET_MARKERS = (
    "mysql+",
    "password=",
    "DATABASE_",
    "sk-",
    "BEGIN RSA",
    "Traceback (most recent call last)",
    "asyncmy",
)


class SkuCheckResult(BaseModel):
    sku: str
    ok: bool
    reason: str


class ToolOutputCheckResult(BaseModel):
    ok: bool
    reason: str


def parse_sku_argument(tool_arguments: str, tool_input: object = None) -> str:
    if isinstance(tool_input, dict):
        raw = tool_input.get("sku")
        if isinstance(raw, str):
            return raw.strip()
    try:
        payload = json.loads(tool_arguments or "{}")
    except json.JSONDecodeError:
        return ""
    raw = payload.get("sku") if isinstance(payload, dict) else None
    return raw.strip() if isinstance(raw, str) else ""


def inspect_sku(sku: str) -> SkuCheckResult:
    value = sku.strip()
    if not value:
        return SkuCheckResult(sku=value, ok=False, reason="empty")
    if len(value) > 32:
        return SkuCheckResult(sku=value, ok=False, reason="too_long")
    if SKU_PATTERN.fullmatch(value) is None:
        return SkuCheckResult(sku=value, ok=False, reason="invalid_format")
    return SkuCheckResult(sku=value, ok=True, reason="ok")


def inspect_tool_output_text(output: object) -> ToolOutputCheckResult:
    text = str(output)
    if any(marker.lower() in text.lower() for marker in _SECRET_MARKERS):
        return ToolOutputCheckResult(ok=False, reason="secret_leak")
    return ToolOutputCheckResult(ok=True, reason="ok")


def evaluate_sku_tool_input(data: ToolInputGuardrailData) -> ToolGuardrailFunctionOutput:
    # @tool_input_guardrail：每次 Tool 调用前执行。Handoff 后专家调 Tool 也会走这里。
    # allow：继续执行 Tool。
    # reject_content：不执行 Tool，把安全说明交给模型继续跑。
    # raise_exception：抛 ToolInputGuardrailTripwireTriggered，中断整次 Run。
    # 常见坑：这不是用户权限校验。user_id / 订单归属仍在 Repository。
    sku = parse_sku_argument(data.context.tool_arguments, data.context.tool_input)
    result = inspect_sku(sku)
    if result.ok:
        return ToolGuardrailFunctionOutput.allow(output_info=result.model_dump())
    return ToolGuardrailFunctionOutput.reject_content(
        "SKU 格式不合法，请使用类似 SKU001 的编号",
        output_info=result.model_dump(),
    )


def evaluate_tool_output_secrets(data: ToolOutputGuardrailData) -> ToolGuardrailFunctionOutput:
    # @tool_output_guardrail：Tool 已经执行完才检查。
    # 不能撤销已经发生的数据库读写。本版库存 Tool 只读，但仍不能把连接串/密钥交回去。
    result = inspect_tool_output_text(data.output)
    if result.ok:
        return ToolGuardrailFunctionOutput.allow(output_info=result.model_dump())
    return ToolGuardrailFunctionOutput.raise_exception(output_info=result.model_dump())


check_sku_tool_input = tool_input_guardrail(name="sku_format")(evaluate_sku_tool_input)
check_tool_output_secrets = tool_output_guardrail(name="tool_secret_filter")(
    evaluate_tool_output_secrets
)
