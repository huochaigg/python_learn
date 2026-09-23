"""
文件作用：V30 概念定位索引。
运行命令：uv run python lessons/v30/concept_index.py
观察重点：按概念找到文件 → 函数。
"""

CONCEPT_INDEX = {
    "Runner.run_streamed": [
        "01_basic_stream_demo.py -> main()",
        "app/services/agent_service.py -> AgentService.stream_chat()",
    ],
    "RunResultStreaming.stream_events": [
        "01_basic_stream_demo.py -> main()",
        "app/services/agent_service.py -> AgentService.stream_chat()",
    ],
    "ResponseTextDeltaEvent": [
        "01_basic_stream_demo.py -> main()",
        "app/services/stream_events.py -> extract_text_delta()",
    ],
    "Tool StreamEvent": [
        "02_tool_stream_demo.py -> main()",
        "app/services/agent_service.py -> AgentService.stream_chat()",
    ],
    "SSE Formatter": [
        "03_sse_format_demo.py -> main()",
        "app/core/sse.py -> encode_sse()",
    ],
    "StreamingResponse": [
        "app/routers/agent_router.py -> stream_chat()",
    ],
    "fetch ReadableStream": [
        "frontend/index.html -> sendMessage()",
    ],
    "AbortController": [
        "frontend/index.html -> stopMessage()",
    ],
    "AsyncSession in stream": [
        "app/routers/agent_router.py -> stream_chat()",
        "app/services/agent_service.py -> AgentService.stream_chat()",
    ],
}


def main() -> None:
    print("===== V30 concept_index =====")
    for name, locs in CONCEPT_INDEX.items():
        print(name)
        for loc in locs:
            print(f"  {loc}")


if __name__ == "__main__":
    main()
