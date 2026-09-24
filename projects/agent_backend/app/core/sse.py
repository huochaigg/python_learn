import json
from typing import Any


def encode_sse(event: str, data: dict[str, Any]) -> str:
    """把应用事件编码成一段 SSE 文本。

    Python dict → json.dumps → SSE 文本 → HTTP Chunk → 浏览器按空行切事件。
    一次 yield 不等于一次客户端 read；一次 read 也不保证刚好一个完整 SSE Event。
    json.dumps 保证中文和特殊字符被正确转义，不要手写伪 JSON。
    """
    payload = json.dumps(data, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


def split_sse_frames(buffer: str) -> tuple[list[str], str]:
    """按空行切出完整 SSE 帧，剩下不完整部分留在 buffer。用于跨 Chunk 解析。"""
    frames: list[str] = []
    while True:
        split_at = None
        for sep in ("\r\n\r\n", "\n\n"):
            idx = buffer.find(sep)
            if idx >= 0 and (split_at is None or idx < split_at[0]):
                split_at = (idx, len(sep))
        if split_at is None:
            break
        idx, sep_len = split_at
        frames.append(buffer[:idx])
        buffer = buffer[idx + sep_len :]
    return frames, buffer


def parse_sse_frame(frame: str) -> tuple[str, str]:
    event_name = "message"
    data_lines: list[str] = []
    for raw_line in frame.splitlines():
        line = raw_line.strip("\r")
        if line.startswith("event:"):
            event_name = line[6:].strip()
        elif line.startswith("data:"):
            data_lines.append(line[5:].lstrip())
    return event_name, "\n".join(data_lines)
