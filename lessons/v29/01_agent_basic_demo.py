"""
文件作用：创建最简单的 Agent，调用 await Runner.run()，打印 final_output。
实际意义：真实项目里 Agent 是可复用的行为配置，真正干活的是 Runner；先跑通这一条，后面才能接 Tool 和数据库。
运行命令：uv run python lessons/v29/01_agent_basic_demo.py
观察重点：终端只出现 final_output 的真实模型回答。
"""

import asyncio

from agents import Agent, Runner

from app.core.config import require_openai_key, settings

# Agent：一组行为配置（name / instructions / tools / model），不是一次 API 调用。
# 和直接调 OpenAI Chat Completions 的区别：你声明「这个助手是谁、怎么做」，
# 由 Runner 负责循环调用模型、处理 tool call，而不是自己写 while True 发 HTTP。
# name：给这个 Agent 的人类可读名字，便于日志/追踪；不是发给用户的品牌文案。
# instructions：系统侧行为说明（类似 system prompt），告诉模型角色和约束。
# 类比 NestJS：Agent ≈ 一组行为配置 + prompt + tools；Runner ≈ 真正执行工作流的 runtime。
# 这只是帮助理解，不是 API 一一对应。
agent = Agent(
    name="Async Tutor",
    instructions="你是 Python 后端助教。用两三句中文解释问题，不要展开成长文。",
    model=settings.openai_model,
)


async def main() -> None:
    require_openai_key()
    # Runner：执行器 / runtime。Agent 是配置，Runner 才真正跑。
    # Runner.run() 是 coroutine：内部可能多次调用模型，必须 await。
    # 它不是「一次 HTTP 请求」的别名；一次 run 可能是 Model →（可选 Tool）→ Model → ...
    # 返回 RunResult：本次 run 的结果对象，不只是字符串。
    # RunResult.final_output：最后一轮模型给出的最终输出。
    result = await Runner.run(agent, "用两三句话解释 Python async/await。")
    print(f"final_output: {result.final_output}")
    assert result.final_output


if __name__ == "__main__":
    asyncio.run(main())
