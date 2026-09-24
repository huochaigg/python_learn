from datetime import datetime

from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1)
    message: str = Field(min_length=1)


class AgentChatResponse(BaseModel):
    conversation_id: str
    answer: str


class ConversationCreateRequest(BaseModel):
    title: str = Field(default="新会话", min_length=1, max_length=120)


class ConversationOut(BaseModel):
    id: str
    user_id: int
    title: str
    status: str
    created_at: datetime
    updated_at: datetime


class MessageOut(BaseModel):
    id: int
    conversation_id: str
    role: str
    content: str
    message_type: str
    status: str
    created_at: datetime
