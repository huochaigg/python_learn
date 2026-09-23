"""
文件作用：用 Runner.run_streamed() + stream_events() 逐段输出模型文本。
实际意义：聊天产品要把 token 增量推到前端，不能等整段回答结束才返回。
运行命令：uv run python lessons/v30/01_basic_stream_demo.py
观察重点：终端逐段出现文字；结束后只打印 is_complete，不再把同一段回答完整打印第二次。
"""

import asyncio

from openai.types.responses import ResponseTextDeltaEvent

from agents import Agent, Runner

from app.core.config import require_openai_key, settings
from app.services.stream_events import extract_text_delta

# Agent 仍是配置。流式执行走 Runner.run_streamed，不是 Runner.run。
agent = Agent(
    name="Stream Tutor",
    instructions="你是 Python 后端助教。用两三句中文解释问题，不要成长文。",
    model=settings.openai_model,
)


async def main() -> None:
    require_openai_key()
    # Runner.run_streamed：流式执行入口。是什么：同步方法，立刻返回 RunResultStreaming。
    # 为什么用：要把模型增量推出去，不能等整段结束。什么时候：需要 SSE/打字机效果时。
    # 参数：agent、用户输入；返回值：RunResultStreaming（不是 coroutine）。
    # 常见坑：写成 await Runner.run_streamed()。JS 类比：调用后立刻拿到 stream 对象，而不是 Promise<完整结果>。
    result = Runner.run_streamed(agent, "用两三句话解释 Python async/await。")
    # stream_events()：异步迭代器。类似 JS async function* + for await...of。
    # 普通 for 不行：它不会 await 下一次事件，拿不到异步流。
    async for event in result.stream_events():
        if event.type != "raw_response_event":
            continue
        # ResponseTextDeltaEvent：助手文本增量。不要把 Function Call 的 arguments delta 当正文。
        # delta：这一小段新文本。final_output：整段结束后的完整答案。二者不要各打印一遍。
        # streaming 不等于每个中文字单独返回，模型按 token/chunk 推送，长度不固定。
        delta = extract_text_delta(event)
        if not delta and isinstance(getattr(event, "data", None), ResponseTextDeltaEvent):
            delta = event.data.delta
        if delta:
            # flush=True：立刻把缓冲区打到终端，否则可能攒一整句才显示，看起来不像流。
            print(delta, end="", flush=True)
    print()
    # 最后一个 delta 不等于 Run 完成。必须消费完 stream_events() 再看 is_complete。
    print(f"is_complete={result.is_complete}")
    print(f"final_output_ready={bool(result.final_output)}")


if __name__ == "__main__":
    asyncio.run(main())
