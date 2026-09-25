from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from agents import UserError, handoff

from app.agents.context import AgentContext
from app.agents.inventory_agent import inventory_agent
from app.agents.run_trace import last_agent_name, list_handoffs, list_tool_names
from app.agents.triage_agent import on_inventory_handoff, on_order_handoff
from app.schemas.handoff import HandoffData, MultiAgentChatResponse
from app.services.agent_service import MULTI_AGENT_MAX_TURNS
from app.services.errors import AgentMaxTurnsError


def test_handoff_data_requires_reason() -> None:
    try:
        HandoffData.model_validate({"reason": ""})
    except ValidationError as extra:
        assert extra.error_count() >= 1
        return
    raise AssertionError("expected ValidationError")


def test_handoff_data_parses() -> None:
    data = HandoffData.model_validate({"reason": "用户问SKU002库存"})
    assert data.reason == "用户问SKU002库存"


def test_input_type_requires_on_handoff() -> None:
    with pytest.raises(UserError):
        handoff(inventory_agent, input_type=HandoffData)


@pytest.mark.asyncio
async def test_on_handoff_records_reason() -> None:
    context = AgentContext(db=MagicMock(), user_id=1)
    wrapper = SimpleNamespace(context=context)
    await on_inventory_handoff(wrapper, HandoffData(reason="查库存"))
    await on_order_handoff(wrapper, HandoffData(reason="查订单"))
    assert context.handoff_reasons == ["inventory:查库存", "order:查订单"]
    assert context.user_id == 1


def test_run_trace_reads_sdk_items() -> None:
    inventory = SimpleNamespace(name="Inventory Agent")
    triage = SimpleNamespace(name="Triage Agent")
    result = SimpleNamespace(
        last_agent=inventory,
        new_items=[
            SimpleNamespace(
                type="handoff_output_item",
                source_agent=triage,
                target_agent=inventory,
            ),
            SimpleNamespace(type="tool_call_item", tool_name="get_product_stock"),
        ],
    )
    assert last_agent_name(result) == "Inventory Agent"
    assert list_handoffs(result) == ["Triage Agent->Inventory Agent"]
    assert list_tool_names(result) == ["get_product_stock"]


def test_multi_agent_http_dto_has_last_agent() -> None:
    body = MultiAgentChatResponse(
        conversation_id="c1",
        answer="库存 8",
        last_agent="Inventory Agent",
        handoffs=["Triage Agent->Inventory Agent"],
        reasons=["inventory:查库存"],
    )
    dumped = body.model_dump()
    assert dumped["last_agent"] == "Inventory Agent"
    assert "answer" in dumped
    assert MULTI_AGENT_MAX_TURNS == 8
    assert AgentMaxTurnsError is not Exception
