from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from agents import Runner
from agents.testing import assistant_message, function_call

from app.agents.run_trace import list_tool_names
from scripted_support import fake_context, scripted_product_agent

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_product_stock_is_really_executed() -> None:
    # 这个测试做什么：验证模型发出 get_product_stock("SKU001") 后，Tool 函数体真的执行。
    # 输入：ScriptedModel 第一步 function_call，第二步最终文本。
    # 内部：patch Repository，避免连 MySQL；Runner 执行真实 Function Tool。
    # 返回：context.tool_calls 记录参数；list_tool_names 看到工具名。
    # 为什么这样写：Tool 测试看「调了哪个、参数对不对、结果有没有进 Agent Loop」，不是看自然语言。
    # 常见坑：只 assert 最终字符串会被假答案骗过；不要用 FakeModel 冒充官方 ScriptedModel。
    product = SimpleNamespace(sku="SKU001", stock=12, name="机械键盘")
    agent, model = scripted_product_agent(
        [
            [function_call("get_product_stock", {"sku": "SKU001"}, call_id="call_stock")],
            [assistant_message("SKU001 当前库存 12")],
        ]
    )
    context = fake_context()
    with patch(
        "app.tools.product_tools.product_repository.get_by_sku",
        AsyncMock(return_value=product),
    ) as lookup:
        result = await Runner.run(agent, "查询 SKU001 库存", context=context, max_turns=6)
    assert context.tool_calls == ["get_product_stock:SKU001"]
    lookup.assert_awaited()
    assert lookup.await_args.args[1] == "SKU001"
    assert "get_product_stock" in list_tool_names(result)
    assert result.final_output == "SKU001 当前库存 12"
    model.assert_complete()
    assert model.remaining_steps == 0
