from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.message import Message


class MessageRepository:
    async def add(self, session: AsyncSession, message: Message) -> Message:
        session.add(message)
        await session.flush()
        return message

    async def get_by_id(self, session: AsyncSession, message_id: int) -> Message | None:
        return await session.get(Message, message_id)

    async def list_by_conversation(
        self, session: AsyncSession, conversation_id: str
    ) -> list[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc(), Message.id.asc())
        )
        return list((await session.execute(stmt)).scalars())

    async def delete_by_conversation(self, session: AsyncSession, conversation_id: str) -> None:
        await session.execute(delete(Message).where(Message.conversation_id == conversation_id))


message_repository = MessageRepository()
