from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..schemas.agent import AgentChatRequest, AgentChatResponse
from ..services.agent_service import agent_service

router = APIRouter(prefix="/agent", tags=["agent"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.post("/chat", response_model=AgentChatResponse)
async def chat(body: AgentChatRequest, db: DbSession) -> AgentChatResponse:
    try:
        answer = await agent_service.chat(db, body.message)
    except Exception as extra:
        raise HTTPException(status_code=500, detail="agent run failed") from extra
    return AgentChatResponse(answer=answer)
