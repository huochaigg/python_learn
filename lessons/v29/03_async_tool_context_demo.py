"""
文件作用：演示 async Function Tool 和 RunContextWrapper 本地 Context。
实际意义：真实后端会把 user、Db Session 这类依赖放在 request context 里给 Tool 用，而不是写进 prompt。
运行命令：uv run python lessons/v29/03_async_tool_context_demo.py
观察重点：Tool 打印 context 里的 username；final_output 基于 Tool Result。Context 本身不会自动出现在模型上下文里。
"""

import asyncio
from dataclasses import dataclass

from agents import Agent, RunContextWrapper, Runner, function_tool

from app.core.config import require_openai_key, settings


@dataclass
class AgentContext:
    user_id: int
    username: str


@function_tool
async def get_current_user_info(ctx: RunContextWrapper[AgentContext]) -> str:
    """返回当前请求用户的本地身份信息。"""
    # RunContextWrapper：SDK 在调用 Tool 时注入的包装对象。
    # wrapper.context：Runner.run(context=...) 传入的 Python 对象（Local Context）。
    # Local Context ≠ LLM Context：API Key、DB Session、用户对象通常不能直接塞进 prompt。
    # 传给 Runner.run(context=...) 不会自动变成模型上下文。
    # 只有本函数的返回值（Tool Result）才会进入后续模型调用。
    await asyncio.sleep(0.1)
    user = ctx.context
    # print('ctx', ctx)
    print(f"tool called: user_id={user.user_id} username={user.username}")
    return f"user_id={user.user_id} username={user.username}"


# Agent[AgentContext]：泛型标明 Local Context 类型，类似 TypeScript 的 Agent<AgentContext>。
agent = Agent[AgentContext](
    name="User Context Agent",
    instructions="用户问自己是谁时，必须调用 get_current_user_info。用中文简短回答。",
    tools=[get_current_user_info],
    model=settings.openai_model,
)


async def main() -> None:
    require_openai_key()
    context = AgentContext(user_id=7, username="ada")
    result = await Runner.run(agent, "我当前是谁？", context=context)
    print(f"final_output: {result.final_output}")
    assert result.final_output
    assert "ada" in str(result.final_output).lower() or "7" in str(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
