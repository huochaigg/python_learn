import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import init_schema, migrate_schema, seed_products
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
    await init_sdk_session_tables()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=90.0,
    ) as ac:
        yield ac


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_plain_chat_still_returns_text(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    created = await client.post("/conversations", headers=headers, json={"title": "v32-chat"})
    assert created.status_code == 200
    cid = created.json()["id"]
    chat = await client.post(
        "/agent/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "用一句话打招呼"},
    )
    assert chat.status_code == 200
    body = chat.json()
    assert body["conversation_id"] == cid
    assert isinstance(body["answer"], str)
    assert body["answer"]


async def test_product_analyze_sku002(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    created = await client.post("/conversations", headers=headers, json={"title": "v32-analyze"})
    cid = created.json()["id"]
    response = await client.post(
        "/agent/product/analyze",
        headers=headers,
        json={"conversation_id": cid, "message": "查询 SKU002 库存，并告诉我能否购买"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "product_stock"
    assert body["data"]["sku"] == "SKU002"
    assert body["data"]["stock"] == 8
    assert body["data"]["can_purchase"] is True


async def test_product_analyze_not_found(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    created = await client.post("/conversations", headers=headers, json={"title": "v32-missing"})
    cid = created.json()["id"]
    response = await client.post(
        "/agent/product/analyze",
        headers=headers,
        json={"conversation_id": cid, "message": "SKU999 还有多少库存？"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "not_found"
    assert body["data"] is None
