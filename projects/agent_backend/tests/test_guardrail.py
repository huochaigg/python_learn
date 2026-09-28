from unittest.mock import AsyncMock, patch

import pytest
from agents import Runner, gen_trace_id, get_current_trace, trace
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.testing import assistant_message, function_call

from app.guardrails.input_guardrails import check_business_scope
from scripted_support import fake_context, scripted_product_agent

pytestmark = pytest.mark.asyncio


async def test_input_guardrail_tripwire_blocks_tools() -> None:
    # 这个测试做什么：危险/跑题请求触发 Input Guardrail tripwire，且阻塞模式下 Tool 不执行。
    # 输入：数学题。内部：clone product_agent 挂上阻塞式 business_scope。
    # 返回：抛 InputGuardrailTripwireTriggered；context.tool_calls 为空。
    # 为什么这样写：V34 的关键保证是「拦住之后 Tool 没跑」，不能只看异常类型。
    # 常见坑：脚本里即使准备了 function_call，tripwire 发生在模型调用前，步骤不会被消费。
    agent, model = scripted_product_agent(
        [
            [function_call("get_product_stock", {"sku": "SKU001"}, call_id="should_not_run")],
            [assistant_message("should not happen")],
        ]
    )
    agent = agent.clone(input_guardrails=[check_business_scope])
    context = fake_context()
    with pytest.raises(InputGuardrailTripwireTriggered):
        await Runner.run(agent, "帮我解一道数学题。", context=context, max_turns=6)
    assert context.tool_calls == []
    assert model.remaining_steps == 2


async def test_tool_guardrail_reject_does_not_execute_tool() -> None:
    # 这个测试做什么：非法 SKU ?? 触发 Tool Input Guardrail reject_content。
    # 输入：脚本调用 get_product_stock("??")。内部：真实 Tool Guardrail 在函数体前拦截。
    # 返回：tool_calls 仍为空（append 在函数体内）；模型用第二步给出最终话术。
    # 为什么这样写：reject_content 不是 tripwire 异常，但 Tool 仍然不能执行。
    # 常见坑：Repository 被 patch 后如果仍被 await，说明 Guardrail 没拦住。
    agent, model = scripted_product_agent(
        [
            [function_call("get_product_stock", {"sku": "??"}, call_id="bad_sku")],
            [assistant_message("SKU 格式不合法")],
        ]
    )
    context = fake_context()
    with patch(
        "app.tools.product_tools.product_repository.get_by_sku",
        AsyncMock(),
    ) as lookup:
        result = await Runner.run(agent, "查询 ?? 的库存", context=context, max_turns=6)
    lookup.assert_not_awaited()
    assert context.tool_calls == []
    assert result.final_output == "SKU 格式不合法"
    model.assert_complete()


async def test_failed_guardrail_run_still_has_trace() -> None:
    # 失败追踪：tripwire 时 Trace context 还在。线上排查失败请求比看成功请求更重要。
    agent, _model = scripted_product_agent([[assistant_message("should not run")]])
    agent = agent.clone(input_guardrails=[check_business_scope])
    context = fake_context()
    trace_id = gen_trace_id()
    with trace("guardrail-fail-workflow", trace_id=trace_id, group_id="conv_fail"):
        with pytest.raises(InputGuardrailTripwireTriggered):
            await Runner.run(agent, "帮我解一道数学题。", context=context, max_turns=6)
        current = get_current_trace()
        assert current is not None
        # 兼容网关会 set_tracing_disabled(True)，此时 trace_id 可能是 no-op。
        # 重点是 tripwire 之后仍在 Trace context 内，且 Tool 没跑。
        assert current.trace_id in {trace_id, "no-op"}
        assert context.tool_calls == []
