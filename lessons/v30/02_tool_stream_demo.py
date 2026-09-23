"""
文件作用：流式消费库存 Agent，观察 Tool Call / Tool Output 与文本 delta。
实际意义：真实库存问答会先调 Tool 查 MySQL，再生成自然语言；前端需要分别展示这两个阶段。
运行命令：uv run python lessons/v30/02_tool_stream_demo.py
观察重点：先出现 tool_call / tool_output，再出现 delta；不要把 message_output_item 再拼一遍。
"""

import asyncio

from agents import Runner

from app.agents.context import AgentContext
from app.agents.product_agent import product_agent
from app.core.config import require_openai_key
from app.core.database import AsyncSessionLocal, engine, init_schema, seed_products
from app.services.stream_events import extract_text_delta


async def main() -> None:
    require_openai_key()
    await init_schema()
    await seed_products()
    async with AsyncSessionLocal() as session:
        context = AgentContext(db=session)
        result = Runner.run_streamed(product_agent, "SKU002 还有多少库存？", context=context)
        printed_delta = False
        async for event in result.stream_events():
            if event.type == "raw_response_event":
                # raw_response_event：底层模型流。文本增量从这里来。
                delta = extract_text_delta(event)
                if delta:
                    if not printed_delta:
                        print("delta:", end=" ", flush=True)
                        printed_delta = True
                    print(delta, end="", flush=True)
                continue
            if event.type == "run_item_stream_event":
                # run_item_stream_event：SDK 处理后的较高级事件（tool / message item）。
                item = event.item
                item_type = getattr(item, "type", "")
                print("__item__: ", item)
                if item_type == "tool_call_item":
                    print(f"tool_call: {item.tool_name or 'get_product_stock'}")
                elif item_type == "tool_call_output_item":
                    print(f"tool_output: {item.output}")
                # message_output_item 是完整消息，已经用 delta 打过，不再打印以免重复。
                continue
            if event.type == "agent_updated_stream_event":
                # 本版不学 Multi-Agent，只确认事件存在。
                print(f"agent_updated: {event.new_agent.name}")
        if printed_delta:
            print()
        print(f"is_complete={result.is_complete}")
        print(f"final_output_ready={bool(result.final_output)}")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
