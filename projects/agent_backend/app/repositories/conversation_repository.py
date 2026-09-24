from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.conversation import Conversation


class ConversationRepository:
    async def create(self, session: AsyncSession, conversation: Conversation) -> Conversation:
        session.add(conversation)
        await session.flush()
        return conversation

    async def get_by_id(self, session: AsyncSession, conversation_id: str) -> Conversation | None:
        return await session.get(Conversation, conversation_id)

    async def get_owned(
        self, session: AsyncSession, conversation_id: str, user_id: int
    ) -> Conversation | None:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        return (await session.execute(stmt)).scalar_one_or_none()

    async def list_by_user(self, session: AsyncSession, user_id: int) -> list[Conversation]:
        stmt = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc(), Conversation.id.desc())
        )
        return list((await session.execute(stmt)).scalars())

    async def touch(self, session: AsyncSession, conversation: Conversation) -> None:
        conversation.updated_at = datetime.now()

    async def delete(self, session: AsyncSession, conversation: Conversation) -> None:
        await session.delete(conversation)


conversation_repository = ConversationRepository()
