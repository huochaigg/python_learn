import asyncio
import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import AsyncSessionLocal, get_db
from ..core.sse import encode_sse
from ..schemas.agent import AgentChatRequest, AgentChatResponse
from ..services.agent_service import agent_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("/chat", response_model=AgentChatResponse)
async def chat(body: AgentChatRequest, db: DbSession) -> AgentChatResponse:
    try:
        answer = await agent_service.chat(db, body.message)
    except Exception as extra:
        raise HTTPException(status_code=500, detail="agent run failed") from extra
    return AgentChatResponse(answer=answer)


@router.post("/chat/stream")
async def stream_chat(body: AgentChatRequest, request: Request) -> StreamingResponse:
    # StreamingResponse：把 async generator 的 yield 写成 HTTP chunk。
    # media_type=text/event-stream 告诉浏览器这是 SSE，不是普通 JSON。
    # 流一旦开始就是 HTTP 200，之后不能再改成 500，错误只能发 event: error。
    request_id = uuid.uuid4().hex

    async def generate():
        yield encode_sse("start", {"request_id": request_id})
        try:
# FastAPI 0.141 / Starlette 1.6：yield Depends 的 AsyncExitStack 会活到流结束，
# 理论上 route 注入 get_db 也能撑过 StreamingResponse。
# 本接口仍把 Session 放在 generator 内，生命周期一眼能看清，不依赖框架细节。
# 与 V29 Depends(get_db) 的区别：V29 等 Runner.run() 结束才返回 JSON；
# 本接口先返回 StreamingResponse，Tool 查库发生在返回之后。
            async with AsyncSessionLocal() as session:
                async for event_name, data in agent_service.stream_chat(session, body.message):
                    if await request.is_disconnected():
                        break
                    yield encode_sse(event_name, data)
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.exception("sse generate failed")
            yield encode_sse(
                "error",
                {"code": "AGENT_STREAM_ERROR", "message": "agent stream failed"},
            )

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
