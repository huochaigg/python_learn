import os
from unittest.mock import MagicMock

from agents import Agent, RunContextWrapper
from agents.exceptions import (
    InputGuardrailTripwireTriggered,
    MaxTurnsExceeded,
    ModelBehaviorError,
    ModelTimeoutError,
    OutputGuardrailTripwireTriggered,
    ToolTimeoutError,
)
from agents.tool import FunctionTool
from agents.tool_context import ToolContext
from agents.tool_guardrails import ToolInputGuardrailData, ToolOutputGuardrailData

from app.agents.context import AgentContext
from app.core.agent_exceptions import (
    AGENT_MAX_TURNS,
    AGENT_MODEL_ERROR,
    AGENT_TIMEOUT,
    INPUT_GUARDRAIL_BLOCKED,
    OUTPUT_GUARDRAIL_BLOCKED,
    map_sdk_exception,
)
from app.core.sse import encode_sse
from app.guardrails.input_guardrails import (
    check_business_scope,
    classify_business_scope,
    evaluate_business_scope,
)
from app.guardrails.output_guardrails import check_final_output, evaluate_final_output, inspect_final_output
from app.guardrails.tool_guardrails import (
    check_sku_tool_input,
    check_tool_output_secrets,
    evaluate_sku_tool_input,
    evaluate_tool_output_secrets,
    inspect_sku,
    inspect_tool_output_text,
)
from app.schemas.product import ProductAnalysis
from app.tools.product_tools import get_product_stock


def _behavior_type(output: object) -> str:
    behavior = getattr(output, "behavior", output)
    if isinstance(behavior, dict):
        return str(behavior.get("type") or "")
    return str(getattr(behavior, "type", behavior))


def test_legal_request_passes_input_guardrail() -> None:
    result = classify_business_scope("帮我查询 SKU002 的库存。")
    assert result.in_scope is True
    ctx = RunContextWrapper(context=AgentContext(db=MagicMock(), user_id=1))
    agent = Agent(name="x", instructions="x")
    output = evaluate_business_scope(ctx, agent, "帮我查询 SKU002 的库存。")
    assert output.tripwire_triggered is False


def test_math_question_triggers_tripwire() -> None:
    result = classify_business_scope("帮我解一道数学题。")
    assert result.in_scope is False
    ctx = RunContextWrapper(context=AgentContext(db=MagicMock(), user_id=1))
    agent = Agent(name="x", instructions="x")
    output = evaluate_business_scope(ctx, agent, "帮我解一道数学题。")
    assert output.tripwire_triggered is True
    assert output.output_info["reason"] == "off_topic"


def test_input_guardrail_is_not_a_tool() -> None:
    assert not isinstance(check_business_scope, FunctionTool)
    assert check_business_scope.run_in_parallel is False


def test_output_guardrail_rejects_negative_stock() -> None:
    bad = inspect_final_output({"sku": "SKU002", "stock": -1, "message": "x"})
    assert bad.ok is False
    good = inspect_final_output(
        ProductAnalysis(sku="SKU002", stock=8, can_purchase=True, message="可买")
    )
    assert good.ok is True
    leak = inspect_final_output(
        ProductAnalysis(sku="SKU002", stock=8, can_purchase=True, message="INTERNAL_TEST")
    )
    assert leak.ok is False
    ctx = RunContextWrapper(context=AgentContext(db=MagicMock(), user_id=1))
    agent = Agent(name="x", instructions="x")
    tripped = evaluate_final_output(ctx, agent, {"sku": "SKU002", "stock": -1, "message": "x"})
    assert tripped.tripwire_triggered is True


def test_tool_input_guardrail_rejects_bad_sku() -> None:
    assert inspect_sku("SKU002").ok is True
    assert inspect_sku("").ok is False
    assert inspect_sku("??").ok is False
    assert inspect_sku("x" * 40).ok is False
    agent = Agent(name="x", instructions="x")
    context = ToolContext(
        context=AgentContext(db=MagicMock(), user_id=1),
        tool_name="get_product_stock",
        tool_call_id="1",
        tool_arguments='{"sku":"??"}',
        tool_input={"sku": "??"},
    )
    output = evaluate_sku_tool_input(ToolInputGuardrailData(context=context, agent=agent))
    assert _behavior_type(output) == "reject_content"


def test_tool_output_guardrail_blocks_secrets() -> None:
    assert inspect_tool_output_text("SKU002 当前库存 8").ok is True
    assert inspect_tool_output_text("mysql+asyncmy://root:secret@127.0.0.1/db").ok is False
    agent = Agent(name="x", instructions="x")
    context = ToolContext(
        context=AgentContext(db=MagicMock(), user_id=1),
        tool_name="get_product_stock",
        tool_call_id="2",
        tool_arguments='{"sku":"SKU002"}',
    )
    output = evaluate_tool_output_secrets(
        ToolOutputGuardrailData(
            context=context,
            agent=agent,
            output="password=super-secret",
        )
    )
    assert _behavior_type(output) == "raise_exception"


def test_guardrail_does_not_replace_business_auth() -> None:
    # 输入看起来像业务问题，并不等于用户有权看 ORD003。
    assert classify_business_scope("订单 ORD003 现在是什么状态？").in_scope is True


def test_exception_mapping() -> None:
    ctx = RunContextWrapper(context=AgentContext(db=MagicMock(), user_id=1))
    agent = Agent(name="x", instructions="x")
    guard_output = evaluate_business_scope(ctx, agent, "帮我解一道数学题。")
    assert guard_output.tripwire_triggered is True
    mapped_input = map_sdk_exception(
        InputGuardrailTripwireTriggered(
            MagicMock(output=guard_output, guardrail=check_business_scope)
        )
    )
    assert mapped_input.code == INPUT_GUARDRAIL_BLOCKED
    assert mapped_input.status_code == 400
    assert "Traceback" not in mapped_input.message
    assert map_sdk_exception(MaxTurnsExceeded("too many")).code == AGENT_MAX_TURNS
    assert map_sdk_exception(ModelBehaviorError("bad")).code == AGENT_MODEL_ERROR
    assert map_sdk_exception(ToolTimeoutError("slow_lookup", 0.05)).code == AGENT_TIMEOUT
    assert map_sdk_exception(ModelTimeoutError(1.2)).code == AGENT_TIMEOUT
    output_mapped = map_sdk_exception(
        OutputGuardrailTripwireTriggered(MagicMock(guardrail=MagicMock()))
    )
    assert output_mapped.code == OUTPUT_GUARDRAIL_BLOCKED


def test_sse_error_event_is_not_done() -> None:
    frame = encode_sse(
        "error",
        {"code": INPUT_GUARDRAIL_BLOCKED, "message": "当前问题不在供应链助手范围内"},
    )
    assert frame.startswith("event: error")
    assert "event: done" not in frame
    assert "INPUT_GUARDRAIL_BLOCKED" in frame


def test_stock_tool_has_guardrails() -> None:
    assert isinstance(get_product_stock, FunctionTool)
    assert get_product_stock.tool_input_guardrails
    assert get_product_stock.tool_output_guardrails


def test_no_api_key_does_not_fake_runner() -> None:
    from app.core.config import settings

    if settings.openai_api_key or os.getenv("OPENAI_API_KEY"):
        return
    # 没有 Key 时本文件的确定性测试已经覆盖 Guardrail 逻辑。
    assert classify_business_scope("帮我解一道数学题。").in_scope is False
