import logging
import uuid

from ..core.database import AsyncSessionLocal
from ..models.conversation import Conversation
from ..models.message import Message
from ..repositories.conversation_repository import conversation_repository
from ..repositories.message_repository import message_repository
from ..sessions.agent_session import get_agent_session
from ..sessions.run_guard import conversation_run_guard
from .errors import ConversationBusy, ConversationDeleteError, ConversationNotFound

logger = logging.getLogger(__name__)


class ConversationService:
    async def create(self, user_id: int, title: str) -> Conversation:
        conversation = Conversation(
            id=uuid.uuid4().hex,
            user_id=user_id,
            title=title,
            status="active",
        )
        async with AsyncSessionLocal() as session:
            await conversation_repository.create(session, conversation)
            await session.commit()
            await session.refresh(conversation)
            return conversation

    async def list_for_user(self, user_id: int) -> list[Conversation]:
        async with AsyncSessionLocal() as session:
            return await conversation_repository.list_by_user(session, user_id)

    async def require_owned(self, conversation_id: str, user_id: int) -> Conversation:
        async with AsyncSessionLocal() as session:
            conversation = await conversation_repository.get_owned(
                session, conversation_id, user_id
            )
        if conversation is None:
            raise ConversationNotFound
        return conversation

    async def list_messages(self, conversation_id: str, user_id: int) -> list[Message]:
        await self.require_owned(conversation_id, user_id)
        async with AsyncSessionLocal() as session:
            return await message_repository.list_by_conversation(session, conversation_id)

    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        status: str,
    ) -> Message:
        async with AsyncSessionLocal() as session:
            conversation = await conversation_repository.get_by_id(session, conversation_id)
            if conversation is None:
                raise ConversationNotFound
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                status=status,
            )
            await message_repository.add(session, message)
            await conversation_repository.touch(session, conversation)
            await session.commit()
            await session.refresh(message)
            return message

    async def finish_message(self, message_id: int, content: str, status: str) -> None:
        async with AsyncSessionLocal() as session:
            message = await message_repository.get_by_id(session, message_id)
            if message is None:
                return
            message.content = content
            message.status = status
            conversation = await conversation_repository.get_by_id(
                session, message.conversation_id
            )
            if conversation is not None:
                await conversation_repository.touch(session, conversation)
            await session.commit()

    async def delete(self, conversation_id: str, user_id: int) -> None:
        await self.require_owned(conversation_id, user_id)
        if conversation_run_guard.is_active(conversation_id):
            raise ConversationBusy
        sdk_session = get_agent_session(conversation_id)
        try:
            await sdk_session.clear_session()
        except Exception as extra:
            logger.exception("sdk session clear failed conversation_id=%s", conversation_id)
            raise ConversationDeleteError("sdk history clear failed") from extra
        try:
            async with AsyncSessionLocal() as session:
                await message_repository.delete_by_conversation(session, conversation_id)
                conversation = await conversation_repository.get_by_id(session, conversation_id)
                if conversation is not None:
                    await conversation_repository.delete(session, conversation)
                await session.commit()
        except Exception as extra:
            logger.exception(
                "business conversation delete failed after sdk clear conversation_id=%s",
                conversation_id,
            )
            raise ConversationDeleteError("business rows delete failed") from extra


conversation_service = ConversationService()
