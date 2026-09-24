import asyncio
import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import AsyncSessionLocal, get_db
from ..core.sse import encode_sse
from ..schemas.agent import AgentChatRequest, AgentChatResponse
from ..schemas.product import ProductAnalyzeRequest, ProductAnalyzeResponse
from ..services.agent_service import agent_service
from ..services.conversation_service import conversation_service
from ..services.errors import (
    BusinessMessageSaveError,
    ConversationBusy,
    ConversationNotFound,
    StructuredOutputError,
)
from ..sessions.run_guard import conversation_run_guard

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["agent"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


def current_user_id(x_user_id: Annotated[int, Header(alias="X-User-Id")] = 1) -> int:
    # 本地开发假设。不是 JWT。会话接口仍用 user_id + conversation_id 校验归属。
    if x_user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid user")
    return x_user_id


UserId = Annotated[int, Depends(current_user_id)]


@router.post("/chat", response_model=AgentChatResponse)
async def chat(body: AgentChatRequest, db: DbSession, user_id: UserId) -> AgentChatResponse:
    try:
        answer = await agent_service.chat(
            db,
            body.message,
            conversation_id=body.conversation_id,
            user_id=user_id,
        )
    except ConversationNotFound as extra:
        raise HTTPException(status_code=404, detail="conversation not found") from extra
    except ConversationBusy as extra:
        raise HTTPException(status_code=409, detail="conversation is busy") from extra
    except BusinessMessageSaveError as extra:
        raise HTTPException(status_code=500, detail="business message save failed") from extra
    except Exception as extra:
        raise HTTPException(status_code=500, detail="agent run failed") from extra
    return AgentChatResponse(conversation_id=body.conversation_id, answer=answer)


@router.post("/product/analyze", response_model=ProductAnalyzeResponse)
async def analyze_product(
    body: ProductAnalyzeRequest, db: DbSession, user_id: UserId
) -> ProductAnalyzeResponse:
    # Agent.output_type 约束模型；response_model 约束 HTTP JSON；二者在 Service 层转换。
    try:
        return await agent_service.analyze_product(
            db,
            body.message,
            conversation_id=body.conversation_id,
            user_id=user_id,
        )
    except ConversationNotFound as extra:
        raise HTTPException(status_code=404, detail="conversation not found") from extra
    except ConversationBusy as extra:
        raise HTTPException(status_code=409, detail="conversation is busy") from extra
    except StructuredOutputError as extra:
        raise HTTPException(status_code=502, detail="structured output invalid") from extra
    except BusinessMessageSaveError as extra:
        raise HTTPException(status_code=500, detail="business message save failed") from extra
    except Exception as extra:
        raise HTTPException(status_code=500, detail="agent run failed") from extra


@router.post("/chat/stream")
async def stream_chat(
    body: AgentChatRequest, request: Request, user_id: UserId
) -> StreamingResponse:
    try:
        await conversation_service.require_owned(body.conversation_id, user_id)
    except ConversationNotFound as extra:
        raise HTTPException(status_code=404, detail="conversation not found") from extra
    if conversation_run_guard.is_active(body.conversation_id):
        raise HTTPException(status_code=409, detail="conversation is busy")

    request_id = uuid.uuid4().hex

    async def generate():
        yield encode_sse(
            "start",
            {"request_id": request_id, "conversation_id": body.conversation_id},
        )
        try:
            async with AsyncSessionLocal() as session:
                async for event_name, data in agent_service.stream_chat(
                    session,
                    body.message,
                    conversation_id=body.conversation_id,
                    user_id=user_id,
                    request=request,
                ):
                    if await request.is_disconnected():
                        break
                    yield encode_sse(event_name, data)
        except ConversationBusy:
            yield encode_sse(
                "error",
                {"code": "CONVERSATION_BUSY", "message": "conversation is busy"},
            )
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
