import pytest
from agents import Agent, Runner
from agents.testing import ScriptedModel, assistant_message

pytestmark = pytest.mark.asyncio


async def test_scripted_agent_returns_fixed_output() -> None:
    # 这个测试做什么：验证 Agent + Runner + ScriptedModel 测试环境能跑通。
    # 输入：固定模型输出 "ok"。内部：Runner.run 消费唯一一步脚本。返回：final_output == "ok"。
    # 为什么这样写：测试的是编排和测试夹具，不是 LLM 智商。
    # 常见坑：不要在这种单测里请求真实模型；ScriptedModel 不会走网络。
    model = ScriptedModel([[assistant_message("ok")]])
    agent = Agent(name="Basic Agent", instructions="只回复 ok。", model=model)
    result = await Runner.run(agent, "ping")
    assert result.final_output == "ok"
    model.assert_complete()


async def test_scripted_streaming_returns_fixed_output() -> None:
    # 流式路径也必须能消费 ScriptedModel。drain stream_events 后读 final_output。
    model = ScriptedModel([[assistant_message("ok")]])
    agent = Agent(name="Basic Stream Agent", instructions="只回复 ok。", model=model)
    streamed = Runner.run_streamed(agent, "ping")
    async for _ in streamed.stream_events():
        pass
    assert streamed.final_output == "ok"
    model.assert_complete()
