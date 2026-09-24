import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from agents import Runner
from agents.exceptions import ModelBehaviorError
from pydantic import ValidationError

from ..agents.context import AgentContext
from ..agents.product_agent import product_agent
from ..agents.product_analysis_agent import product_analysis_agent
from ..repositories.product_repository import product_repository
from ..schemas.product import ProductAnalyzeResponse, ProductStockData, ProductStockResult
from ..sessions.agent_session import get_agent_session
from ..sessions.run_guard import conversation_run_guard
from .conversation_service import conversation_service
from .errors import BusinessMessageSaveError, ConversationBusy, StructuredOutputError
from .stream_events import extract_text_delta, public_tool_result

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(
        self,
        session: AsyncSession,
        message: str,
        *,
        conversation_id: str,
        user_id: int,
    ) -> str:
        await conversation_service.require_owned(conversation_id, user_id)
        if not await conversation_run_guard.try_acquire(conversation_id):
            raise ConversationBusy
        await conversation_service.add_message(conversation_id, "user", message, "completed")
        assistant: Any = None
        try:
            # session=sdk_session：Runner 自己 get_items() 再 add_items()。
            # 不要再手动查出历史拼进 input，否则会把同一段上下文传两遍。
            sdk_session = get_agent_session(conversation_id)
            context = AgentContext(db=session, user_id=user_id)
            result = await Runner.run(
                product_agent,
                message,
                context=context,
                session=sdk_session,
            )
            answer = str(result.final_output or "")
            try:
                assistant = await conversation_service.add_message(
                    conversation_id, "assistant", answer, "completed"
                )
            except Exception as extra:
                logger.exception(
                    "business assistant message save failed conversation_id=%s",
                    conversation_id,
                )
                raise BusinessMessageSaveError from extra
            return answer
        except BusinessMessageSaveError:
            raise
        except Exception:
            logger.exception("Runner.run failed conversation_id=%s", conversation_id)
            if assistant is None:
                try:
                    await conversation_service.add_message(
                        conversation_id, "assistant", "", "failed"
                    )
                except Exception:
                    logger.exception("failed assistant message save also failed")
            raise
        finally:
            await conversation_run_guard.release(conversation_id)

    async def stream_chat(
        self,
        session: AsyncSession,
        message: str,
        *,
        conversation_id: str,
        user_id: int,
        request: Request | None = None,
    ) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        await conversation_service.require_owned(conversation_id, user_id)
        if not await conversation_run_guard.try_acquire(conversation_id):
            raise ConversationBusy
        await conversation_service.add_message(conversation_id, "user", message, "completed")
        pending = await conversation_service.add_message(
            conversation_id, "assistant", "", "pending"
        )
        answer_parts: list[str] = []
        final_answer = ""
        completed = False
        sdk_session = get_agent_session(conversation_id)
        context = AgentContext(db=session, user_id=user_id)
        result = Runner.run_streamed(
            product_agent,
            message,
            context=context,
            session=sdk_session,
        )
        last_tool_name = "tool"

        async def drain_cancelled_run() -> None:
            result.cancel()
            async for _ in result.stream_events():
                pass

        async def mark_assistant(status: str, content: str) -> None:
            try:
                await conversation_service.finish_message(pending.id, content, status)
            except Exception:
                logger.exception(
                    "assistant message status update failed conversation_id=%s status=%s",
                    conversation_id,
                    status,
                )

        async def persist_failed() -> None:
            # HTTP 取消会取消当前 Task；必须把 failed 写完再把 CancelledError 抛回去。
            task = asyncio.ensure_future(mark_assistant("failed", "".join(answer_parts)))
            cancelled: asyncio.CancelledError | None = None
            while not task.done():
                try:
                    await asyncio.wait({task})
                except asyncio.CancelledError as extra:
                    if cancelled is None:
                        cancelled = extra
            if cancelled is not None:
                raise cancelled

        try:
            async for event in result.stream_events():
                if request is not None and await request.is_disconnected():
                    await drain_cancelled_run()
                    await mark_assistant("failed", "".join(answer_parts))
                    return
                if event.type == "raw_response_event":
                    delta = extract_text_delta(event)
                    if delta:
                        answer_parts.append(delta)
                        yield ("delta", {"content": delta})
                    continue
                if event.type == "run_item_stream_event":
                    item = event.item
                    item_type = getattr(item, "type", "")
                    if item_type == "tool_call_item":
                        last_tool_name = getattr(item, "tool_name", None) or "tool"
                        yield ("tool_call", {"name": last_tool_name})
                    elif item_type == "tool_call_output_item":
                        yield (
                            "tool_result",
                            {
                                "name": last_tool_name,
                                "result": public_tool_result(getattr(item, "output", "")),
                            },
                        )
                    continue
            if request is not None and await request.is_disconnected():
                await mark_assistant("failed", "".join(answer_parts))
                return
            if not result.is_complete:
                await mark_assistant("failed", "".join(answer_parts))
                yield (
                    "error",
                    {"code": "AGENT_STREAM_INCOMPLETE", "message": "stream not complete"},
                )
                return
            final_answer = str(result.final_output or "".join(answer_parts))
            try:
                await conversation_service.finish_message(pending.id, final_answer, "completed")
                completed = True
            except Exception:
                logger.exception(
                    "business assistant message save failed conversation_id=%s",
                    conversation_id,
                )
                await mark_assistant("failed", final_answer)
                yield (
                    "error",
                    {
                        "code": "BUSINESS_MESSAGE_SAVE_ERROR",
                        "message": "answer generated but business message save failed",
                    },
                )
                return
            yield ("done", {"conversation_id": conversation_id, "answer": final_answer})
        except asyncio.CancelledError:
            if not completed:
                await persist_failed()
            await drain_cancelled_run()
            raise
        except GeneratorExit:
            if not completed:
                await persist_failed()
            await drain_cancelled_run()
            raise
        except Exception:
            logger.exception("Runner.run_streamed failed conversation_id=%s", conversation_id)
            await mark_assistant("failed", "".join(answer_parts))
            yield (
                "error",
                {"code": "AGENT_STREAM_ERROR", "message": "agent stream failed"},
            )
        finally:
            await conversation_run_guard.release(conversation_id)

    def _parse_stock_result(self, final_output: Any) -> ProductStockResult:
        if isinstance(final_output, ProductStockResult):
            return final_output
        try:
            return ProductStockResult.model_validate(final_output)
        except ValidationError as extra:
            raise StructuredOutputError from extra

    async def _to_analyze_response(
        self,
        session: AsyncSession,
        conversation_id: str,
        parsed: ProductStockResult,
    ) -> ProductAnalyzeResponse:
        # Agent.output_type → Service 用数据库重算 can_purchase → HTTP DTO。
        # 模型数字不能直接当下游单权限。
        if parsed.type == "product_stock" and parsed.data is not None:
            product = await product_repository.get_by_sku(session, parsed.data.sku.strip().upper())
            if product is None:
                return ProductAnalyzeResponse(
                    conversation_id=conversation_id,
                    type="not_found",
                    message=f"没有找到 SKU={parsed.data.sku} 的商品",
                    data=None,
                )
            return ProductAnalyzeResponse(
                conversation_id=conversation_id,
                type="product_stock",
                message=parsed.message,
                data=ProductStockData(
                    sku=product.sku,
                    stock=product.stock,
                    can_purchase=product.stock > 0,
                ),
            )
        return ProductAnalyzeResponse(
            conversation_id=conversation_id,
            type=parsed.type,
            message=parsed.message,
            data=None,
        )

    async def analyze_product(
        self,
        session: AsyncSession,
        message: str,
        *,
        conversation_id: str,
        user_id: int,
    ) -> ProductAnalyzeResponse:
        await conversation_service.require_owned(conversation_id, user_id)
        if not await conversation_run_guard.try_acquire(conversation_id):
            raise ConversationBusy
        await conversation_service.add_message(conversation_id, "user", message, "completed")
        try:
            sdk_session = get_agent_session(conversation_id)
            context = AgentContext(db=session, user_id=user_id)
            try:
                result = await Runner.run(
                    product_analysis_agent,
                    message,
                    context=context,
                    session=sdk_session,
                )
            except ModelBehaviorError as extra:
                logger.exception("structured output invalid conversation_id=%s", conversation_id)
                await conversation_service.add_message(
                    conversation_id, "assistant", "", "failed", message_type="text"
                )
                raise StructuredOutputError from extra
            parsed = self._parse_stock_result(result.final_output)
            response = await self._to_analyze_response(session, conversation_id, parsed)
            try:
                await conversation_service.add_message(
                    conversation_id,
                    "assistant",
                    response.model_dump_json(),
                    "completed",
                    message_type=response.type,
                )
            except Exception as extra:
                logger.exception(
                    "business assistant message save failed conversation_id=%s",
                    conversation_id,
                )
                raise BusinessMessageSaveError from extra
            return response
        except (StructuredOutputError, BusinessMessageSaveError, ConversationBusy):
            raise
        except Exception:
            logger.exception("analyze_product failed conversation_id=%s", conversation_id)
            try:
                await conversation_service.add_message(
                    conversation_id, "assistant", "", "failed", message_type="text"
                )
            except Exception:
                logger.exception("failed assistant message save also failed")
            raise
        finally:
            await conversation_run_guard.release(conversation_id)


agent_service = AgentService()
