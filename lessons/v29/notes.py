"""
文件作用：V29 速查。Agent / Runner / Tool / Context / Session 分层。
运行命令：uv run python lessons/v29/notes.py
观察重点：能画出 HTTP → Service → Runner.run → Tool → Repository → MySQL → final_output。
"""

from agents import Agent

# 只构造配置对象，不调用 Runner.run，所以不需要 API Key。
_notes_agent = Agent(name="notes-example", instructions="unused")

NOTES = """
Agent
  行为配置：name + instructions + tools + model。可模块级复用。
  不是一次 HTTP 请求。类比 NestJS：配置 + prompt + 能力声明，不是 runtime。

Runner
  执行器 / runtime。类比 Agent Orchestrator。
  Runner.run() 异步，FastAPI 用这个。
  Runner.run_sync() 同步封装，本版不用。
  Runner.run_streamed() 流式，留给后续 SSE。

Agent Loop（一次 Runner.run 内部）
  User Input + instructions + Tools Schema → Model
  若直接回答 → final_output → RunResult
  若要调 Tool → Runner 校验参数 → 调用真实 Python 函数
    → Tool Result 加入本次 run → 再次调用 Model
    → 继续调 Tool 或输出最终答案
  Runner.run() ≠ 一次 OpenAI HTTP 请求。

RunResult.final_output
  最终输出。RunResult 还承载其它运行信息，本版只取 final_output。

function_tool
  把后端函数声明成 LLM 可发现、可调用的能力。
  函数名 → tool name；类型注解 → JSON Schema；docstring → description。
  真正执行 Python 的是 Runner / SDK，不是模型。

RunContextWrapper / Local Context
  wrapper.context 是 Python 应用内部对象。
  传给 Runner.run(context=...) 不会自动变成模型上下文。
  Tool 返回值才会进入 LLM Context。
  Agent[AgentContext] ≈ TypeScript Agent<AgentContext>。

AsyncSession
  request-scoped。可放进本次 AgentContext，不能放进全局 Agent。
  同一个 Session 不要给多个并发 Task 共用。
  Runner.run 必须在 get_db() 的 session 存活期间完成。

分层
  Router HTTP
  Service 编排 Runner.run
  Agent 行为定义
  Tool 业务能力（窄接口，不要 execute_sql）
  Repository 数据库访问
"""


def main() -> None:
    print(f"notes_agent_name={_notes_agent.name}")
    print(NOTES)


if __name__ == "__main__":
    main()
