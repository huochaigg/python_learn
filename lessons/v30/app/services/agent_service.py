import asyncio
import logging
from collections.abc import AsyncIterator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from agents import Runner

from ..agents.context import AgentContext
from ..agents.product_agent import product_agent
from .stream_events import extract_text_delta, public_tool_result

logger = logging.getLogger(__name__)


class AgentService:
    async def chat(self, session: AsyncSession, message: str) -> str:
        context = AgentContext(db=session)
        try:
            result = await Runner.run(product_agent, message, context=context)
        except Exception:
            logger.exception("Runner.run failed")
            raise
        return str(result.final_output)

    async def stream_chat(
        self, session: AsyncSession, message: str
    ) -> AsyncIterator[tuple[str, dict[str, Any]]]:
        # Runner.run_streamed() 立刻返回 RunResultStreaming，不要 await。
        # 真正的事件在 result.stream_events() 里，必须 async for 消费。
        context = AgentContext(db=session)
        result = Runner.run_streamed(product_agent, message, context=context)
        last_tool_name = "tool"

        async def drain_cancelled_run() -> None:
            # 官方要求 cancel() 后继续消费 stream_events() 完成清理。
            result.cancel()
            async for _ in result.stream_events():
                pass

        try:
            async for event in result.stream_events():
                if event.type == "raw_response_event":
                    delta = extract_text_delta(event)
                    if delta:
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
                    # 跳过 message_output_item：完整文本已通过 delta 发给前端，再发会重复。
                    continue
                # agent_updated_stream_event：本版不学 Multi-Agent，忽略即可。
            if not result.is_complete:
                yield (
                    "error",
                    {"code": "AGENT_STREAM_INCOMPLETE", "message": "stream not complete"},
                )
                return
            yield ("done", {"answer": str(result.final_output or "")})
        except asyncio.CancelledError:
            await drain_cancelled_run()
            raise
        except GeneratorExit:
            await drain_cancelled_run()
            raise
        except Exception:
            logger.exception("Runner.run_streamed failed")
            yield (
                "error",
                {"code": "AGENT_STREAM_ERROR", "message": "agent stream failed"},
            )


agent_service = AgentService()
