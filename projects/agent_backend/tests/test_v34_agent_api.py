import os

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.core.database import init_schema, migrate_schema, seed_orders, seed_products
from app.core.sse import parse_sse_frame, split_sse_frames
from app.main import app
from app.sessions.agent_session import init_sdk_session_tables
from app.services.conversation_service import conversation_service


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


async def _new_conversation(client: AsyncClient, title: str) -> str:
    created = await client.post(
        "/conversations",
        headers={"X-User-Id": "1"},
        json={"title": title},
    )
    assert created.status_code == 200
    return created.json()["id"]


async def test_guarded_chat_allows_stock_query(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v34-ok")
    response = await client.post(
        "/agent/guarded/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "帮我查询 SKU002 的库存。"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["conversation_id"] == cid
    assert "8" in body["answer"]
    rows = await conversation_service.list_messages(cid, 1)
    assistant = [row for row in rows if row.role == "assistant"]
    assert assistant
    assert assistant[-1].status == "completed"


async def test_guarded_chat_blocks_math_and_marks_rejected(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v34-block")
    response = await client.post(
        "/agent/guarded/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "帮我解一道数学题。"},
    )
    assert response.status_code == 400
    body = response.json()
    assert body["code"] == "INPUT_GUARDRAIL_BLOCKED"
    assert "Traceback" not in body["message"]
    rows = await conversation_service.list_messages(cid, 1)
    assistant = [row for row in rows if row.role == "assistant"]
    assert assistant
    assert assistant[-1].status == "rejected"
    assert assistant[-1].status != "completed"


async def test_guarded_stream_emits_error_not_done(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v34-stream")
    response = await client.post(
        "/agent/guarded/stream",
        headers=headers,
        json={"conversation_id": cid, "message": "帮我解一道数学题。"},
    )
    assert response.status_code == 200
    text = response.text
    frames, _ = split_sse_frames(text if text.endswith("\n\n") else text + "\n\n")
    events = [parse_sse_frame(frame)[0] for frame in frames]
    assert "start" in events
    assert "error" in events
    assert "done" not in events


async def test_old_chat_still_works(client: AsyncClient) -> None:
    if not _has_key():
        pytest.skip("缺少 OPENAI_API_KEY")
    headers = {"X-User-Id": "1"}
    cid = await _new_conversation(client, "v34-old")
    chat = await client.post(
        "/agent/chat",
        headers=headers,
        json={"conversation_id": cid, "message": "用一句话打招呼"},
    )
    assert chat.status_code == 200
    assert chat.json()["answer"]
