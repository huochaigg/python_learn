import os
from unittest.mock import AsyncMock, patch

import pytest
from agents.exceptions import MaxTurnsExceeded
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import init_schema, migrate_schema, seed_orders, seed_products
from app.main import app
from app.sessions.agent_session import init_sdk_session_tables


pytestmark = pytest.mark.asyncio


def _has_key() -> bool:
    return bool(settings.openai_api_key or os.getenv("OPENAI_API_KEY"))


@pytest.fixture
async def client():
    await init_schema()
    await migrate_schema()
    await seed_products()
    await seed_orders()
    await init_sdk_session_tables()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=120.0,
    ) as ac:
        yield ac


async def _new_conversation(client: AsyncClient, title: str, user_id: str = "1") -> str:
    headers = {"X-User-Id": user_id}
    created = await client.post("/conversations", headers=headers, json={"title": title})
    assert created.status_code == 200
    return created.json()["id"]


async def test_old_chat_and_analyze_still_work(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-old")
    chat = await client.post(
        "/agent/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "用一句话打招呼"},
    )
    assert chat.status_code == 200
    assert isinstance(chat.json()["answer"], str)
    analyze = await client.post(
        "/agent/product/analyze",
        headers=headers,
        json={"conversation_id": cid, "message": "查询 SKU002 库存，并告诉我能否购买"},
    )
    assert analyze.status_code == 200
    body = analyze.json()
    assert body["type"] == "product_stock"
    assert body["data"]["sku"] == "SKU002"
    assert body["data"]["stock"] == 8


async def test_inventory_request_handoff(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-inventory")
    response = await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "SKU002 还有多少库存？"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["conversation_id"] == cid
    assert body["last_agent"] == "Inventory Agent"
    assert any("Inventory Agent" in item for item in body["handoffs"])
    assert any(item.startswith("inventory:") for item in body["reasons"])
    assert "8" in body["answer"]


async def test_order_request_handoff(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-order")
    response = await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "订单 ORD001 现在是什么状态？"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["last_agent"] == "Order Agent"
    assert any("Order Agent" in item for item in body["handoffs"])
    assert any(item.startswith("order:") for item in body["reasons"])


async def test_missing_sku_and_order_are_safe(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-missing")
    sku = await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "SKU999 还有多少库存？"},
    )
    assert sku.status_code == 200
    assert sku.json()["answer"]
    assert "Traceback" not in sku.json()["answer"]
    order = await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "订单 ORD999 现在是什么状态？"},
    )
    assert order.status_code == 200
    assert order.json()["answer"]
    assert "Traceback" not in order.json()["answer"]


async def test_foreign_order_does_not_leak(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-auth")
    response = await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "订单 ORD003 现在是什么状态？"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "delivered" not in body["answer"].lower()
    assert "Traceback" not in body["answer"]


async def test_conversation_history_is_isolated(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    first = await _new_conversation(client, "v33-iso-a")
    second = await _new_conversation(client, "v33-iso-b")
    await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": first, "message": "SKU002 还有多少库存？暗号是 ALPHA-ISO"},
    )
    await client.post(
        "/agent/multi/chat",
        headers=headers,
        json={"conversation_id": second, "message": "订单 ORD001 现在是什么状态？暗号是 BETA-ISO"},
    )
    first_messages = await client.get(f"/conversations/{first}/messages", headers=headers)
    second_messages = await client.get(f"/conversations/{second}/messages", headers=headers)
    assert first_messages.status_code == 200
    assert second_messages.status_code == 200
    first_text = " ".join(row["content"] for row in first_messages.json())
    second_text = " ".join(row["content"] for row in second_messages.json())
    assert "ALPHA-ISO" in first_text
    assert "BETA-ISO" in second_text
    assert "BETA-ISO" not in first_text
    assert "ALPHA-ISO" not in second_text


async def test_max_turns_returns_safe_http_error(client: AsyncClient) -> None:
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v33-turns")
    with patch(
        "app.services.agent_service.Runner.run",
        new=AsyncMock(side_effect=MaxTurnsExceeded("too many turns")),
    ):
        response = await client.post(
            "/agent/multi/chat",
            headers=headers,
            json={"conversation_id": cid, "message": "SKU002 还有多少库存？"},
        )
    assert response.status_code == 502
    assert response.json()["detail"] == "too many agent turns"
