"""
文件作用：V30 自测题。只问不答。
运行命令：uv run python lessons/v30/checklist.py
观察重点：能从 run_streamed 追到 SSE，再追到 fetch reader。
"""

CHECKLIST = [
    "能解释 Runner.run 与 run_streamed 的区别",
    "知道 run_streamed 不直接 await",
    "知道为什么 stream_events 使用 async for",
    "能解释 raw_response_event",
    "能解释 run_item_stream_event",
    "能读取 ResponseTextDeltaEvent.delta",
    "能观察真实 Tool Call / Tool Output",
    "能解释 SDK Streaming 与 SSE 的区别",
    "能解释 StreamingResponse",
    "能写 Async Generator",
    "能写 SSE Formatter",
    "知道一次 HTTP Chunk 不等于一个 SSE Event",
    "能通过 fetch + ReadableStream 正确解析 SSE",
    "知道如何处理中文和跨 Chunk",
    "知道如何使用 AbortController",
    "知道 HTTP 200 后不能再改状态码",
    "能解释 AsyncSession 在流式响应中的生命周期",
    "知道最后一个 delta 不等于 Run 完成",
    "能用真实 MySQL 完成一次流式库存查询",
]


def main() -> None:
    print("===== V30 checklist（先自己答）=====")
    for index, item in enumerate(CHECKLIST, start=1):
        print()
        print(f"{index}. {item}")
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v30 checklist 运行完毕 ---")
