from agents import Runner, handoff
from agents.handoffs import Handoff
from agents.testing import ScriptedModel, assistant_message, function_call

from app.agents.context import AgentContext
from app.agents.inventory_agent import inventory_agent
from app.agents.run_trace import last_agent_name, list_handoffs
from app.agents.triage_agent import on_inventory_handoff, triage_agent
from app.schemas.handoff import HandoffData
from scripted_support import fake_context

import pytest

pytestmark = pytest.mark.asyncio


async def test_inventory_question_handoffs_to_inventory_agent() -> None:
    # 这个测试做什么：验证 Triage 对库存问题会真实 Handoff 到 Inventory Agent。
    # 输入：Triage 脚本发出 transfer_to_inventory_agent；Inventory 脚本给出最终回答。
    # 内部：clone 两个 Agent 并换 ScriptedModel，避免打到真实模型和模块级全局对象。
    # 返回：result.last_agent、handoff_output_item、on_handoff 写入的 reason。
    # 为什么这样写：不能靠 assert "库存" in final_output 猜测是否交接。
    # 常见坑：Handoff tool 名是 transfer_to_{snake_case(agent.name)}；input_type 必须带 reason。
    inventory_model = ScriptedModel([[assistant_message("已从库存专家回答")]])
    inventory = inventory_agent.clone(model=inventory_model)
    handoff_name = Handoff.default_tool_name(inventory)
    triage_model = ScriptedModel(
        [
            [
                function_call(
                    handoff_name,
                    {"reason": "用户查询 SKU001 库存"},
                    call_id="handoff_inventory",
                )
            ]
        ]
    )
    triage = triage_agent.clone(
        model=triage_model,
        handoffs=[
            handoff(
                inventory,
                on_handoff=on_inventory_handoff,
                input_type=HandoffData,
            )
        ],
    )
    context = fake_context()
    result = await Runner.run(triage, "SKU001 还有多少库存？", context=context, max_turns=8)
    assert last_agent_name(result) == "Inventory Agent"
    assert list_handoffs(result) == ["Triage Agent->Inventory Agent"]
    assert context.handoff_reasons == ["inventory:用户查询 SKU001 库存"]
    assert result.final_output == "已从库存专家回答"
    triage_model.assert_complete()
    inventory_model.assert_complete()
    assert isinstance(context, AgentContext)
