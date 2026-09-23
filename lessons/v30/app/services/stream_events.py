from __future__ import annotations

from typing import Any

from openai.types.responses import ResponseTextDeltaEvent

from agents.stream_events import StreamEvent


def extract_text_delta(event: StreamEvent) -> str | None:
    """从 raw_response_event 取出助手文本增量。

    只认 ResponseTextDeltaEvent（type=response.output_text.delta）。
    Function Call 的 arguments delta 也有 .delta 字符串，不能当正文。
    """
    if getattr(event, "type", None) != "raw_response_event":
        return None
    data = getattr(event, "data", None)
    if isinstance(data, ResponseTextDeltaEvent):
        return data.delta or None
    if getattr(data, "type", None) == "response.output_text.delta":
        delta = getattr(data, "delta", None)
        return delta if isinstance(delta, str) and delta else None
    return None


def public_tool_result(output: Any) -> str:
    text = str(output)
    if len(text) > 300:
        return text[:300] + "..."
    return text
