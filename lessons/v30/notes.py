"""
文件作用：V30 速查。SDK Streaming、SSE、ReadableStream、取消。
运行命令：uv run python lessons/v30/notes.py
观察重点：能画出 Runner.run_streamed → stream_events → encode_sse → fetch reader。
"""

from app.core.sse import encode_sse

_example = encode_sse("delta", {"content": "hi"})

NOTES = """
Runner.run() vs Runner.run_streamed()
  run：等整段结束，返回 RunResult。
  run_streamed：立刻返回 RunResultStreaming，不要 await。
  真正事件在 result.stream_events()。

stream_events + async for
  异步迭代器。类似 JS async function* + for await。
  普通 for 不能 await 下一次事件。

ResponseTextDeltaEvent
  raw_response_event 里的文本增量。delta 是这一小段，不是最终答案。
  streaming 不等于每个中文字单独返回。

raw_response_event
  底层模型流。

run_item_stream_event
  SDK 处理后的 item：tool_call_item / tool_call_output_item / message_output_item。
  Tool Calling 不是普通文本 delta。
  Tool Result 不一定等于最终回复。
  不要把 message_output_item 再和 delta 拼一次。

StreamingResponse + Async Generator
  Python: async def gen(): yield ...
  JS: async function* gen() { yield ... }
  FastAPI 把 yield 写成 HTTP chunk。

SSE
  文本协议：event: / data: / id: / retry: ，两个换行结束事件。
  不是 WebSocket，也不是 SDK Streaming。
  SDK Streaming 在服务端内部；SSE 把应用事件送给浏览器。
  EventSource 适合 GET；本版 Agent 用 POST JSON，所以用 fetch。

fetch + ReadableStream + TextDecoder
  类比 JS/TS 里读 Response.body。
  一次 read 可能半个事件，或多个事件。
  UTF-8 中文可能被拆开，必须 stream: true 再拼 buffer。

AbortController
  前端 abort 只取消 HTTP。不等于 Agent 已成功，也不等于数据库 rollback。
  只读库存 Tool 没有下单副作用。
  cancel() 后要继续消费 stream_events() 做清理。

is_complete / final_output / done
  最后一个 delta ≠ Run 完成。
  消费完 stream_events 再看 is_complete，再发应用层 event: done。
  HTTP 200 已经发出后不能再改成 500，只能 SSE error。

AsyncSession
  流式响应返回后内容还在生成。Session 必须活到 Tool 查完库。
  本版在 generator 里 async with AsyncSessionLocal()。
  不要把 Session 放进全局 Agent，也不要给多个 Task 共用。
"""


def main() -> None:
    print(f"example_sse={_example!r}")
    print(NOTES)


if __name__ == "__main__":
    main()
