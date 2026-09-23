"""
文件作用：用 encode_sse 演示 SSE 文本格式，并用跨 Chunk buffer 解析。
实际意义：浏览器不会按「一次 read = 一个事件」收包；服务端必须先把应用事件编码成 SSE，前端再按空行重装。
运行命令：uv run python lessons/v30/03_sse_format_demo.py
观察重点：编码后的 event/data/空行；被拆开的 chunk 仍能解析出完整 JSON。
"""

import codecs
import json

from app.core.sse import encode_sse, parse_sse_frame, split_sse_frames


def main() -> None:
    frame = encode_sse("delta", {"content": "你好"})
    print(repr(frame))

    # 两个换行结束一个事件。下面把一个完整事件拆到两个 HTTP chunk 里。
    chunks = [frame[:18], frame[18:], encode_sse("done", {"answer": "你好"})]
    buffer = ""
    parsed: list[tuple[str, str]] = []
    for chunk in chunks:
        buffer += chunk
        frames, buffer = split_sse_frames(buffer)
        for raw in frames:
            parsed.append(parse_sse_frame(raw))
    print(f"leftover={buffer!r}")
    for event_name, data in parsed:
        print(f"{event_name} {data}")
        json.loads(data)

    # UTF-8 中文可能被拆到两个 byte chunk；必须增量 decode 再按空行切事件。
    raw_bytes = encode_sse("delta", {"content": "你好"}).encode("utf-8")
    decoder = codecs.getincrementaldecoder("utf-8")()
    text = decoder.decode(raw_bytes[:12]) + decoder.decode(raw_bytes[12:], final=True)
    frames, leftover = split_sse_frames(text)
    event_name, data = parse_sse_frame(frames[0])
    print(f"utf8_split={event_name} {data} leftover={leftover!r}")


if __name__ == "__main__":
    main()
