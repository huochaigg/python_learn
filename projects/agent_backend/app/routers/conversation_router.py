from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException

from ..schemas.agent import ConversationCreateRequest, ConversationOut, MessageOut
from ..services.conversation_service import conversation_service
from ..services.errors import ConversationBusy, ConversationDeleteError, ConversationNotFound

router = APIRouter(prefix="/conversations", tags=["conversations"])


def current_user_id(x_user_id: Annotated[int, Header(alias="X-User-Id")] = 1) -> int:
    if x_user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid user")
    return x_user_id


UserId = Annotated[int, Depends(current_user_id)]


@router.post("", response_model=ConversationOut)
async def create_conversation(
    body: ConversationCreateRequest, user_id: UserId
) -> ConversationOut:
    conversation = await conversation_service.create(user_id, body.title)
    return ConversationOut.model_validate(conversation, from_attributes=True)


@router.get("", response_model=list[ConversationOut])
async def list_conversations(user_id: UserId) -> list[ConversationOut]:
    rows = await conversation_service.list_for_user(user_id)
    return [ConversationOut.model_validate(row, from_attributes=True) for row in rows]


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
async def list_messages(conversation_id: str, user_id: UserId) -> list[MessageOut]:
    try:
        rows = await conversation_service.list_messages(conversation_id, user_id)
    except ConversationNotFound as extra:
        raise HTTPException(status_code=404, detail="conversation not found") from extra
    return [MessageOut.model_validate(row, from_attributes=True) for row in rows]


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, user_id: UserId) -> dict[str, str]:
    try:
        await conversation_service.delete(conversation_id, user_id)
    except ConversationNotFound as extra:
        raise HTTPException(status_code=404, detail="conversation not found") from extra
    except ConversationBusy as extra:
        raise HTTPException(status_code=409, detail="conversation is busy") from extra
    except ConversationDeleteError as extra:
        raise HTTPException(status_code=500, detail="conversation delete failed") from extra
    return {"status": "deleted"}
