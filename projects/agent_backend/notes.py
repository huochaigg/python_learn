"""
文件作用：长期知识索引。按版本追加，不覆盖旧条目。
运行命令：uv run python projects/agent_backend/notes.py
观察重点：V34 能分清 Guardrail、Pydantic 和 Repository 权限。
"""

NOTES = """
[V31] SDK Session / SQLAlchemySession / Conversation / Message
  session_id = conversation_id。Agent Session ≠ AsyncSession ≠ AgentContext。

[V32] Agent.output_type
  把 Pydantic BaseModel 编成 JSON Schema 交给模型。
  Runner 结束后 final_output 是校验过的对象，不必 json.loads。
  TypedDict/dataclass 也能用；本版优先 BaseModel，因为 Field、校验、FastAPI 一体。
  类比 NestJS DTO / class-validator，但约束的是模型输出。

[V32] Tool Result vs Final Output
  Tool：从 MySQL 拿可信库存。
  Agent：理解问题并填 Structured Output。
  Service：用数据库再算 can_purchase，模型不能当最终下单许可。

[V32] 三种校验
  Pydantic ValidationError：本地 schema。
  SDK Structured Output / ModelBehaviorError：模型没产出合法 JSON。
  业务库存错误：商品不存在、stock 事实。合法 Schema 也可以是错误事实。

[V32] output_type vs response_model vs model_validate
  output_type 约束模型。
  response_model 约束 HTTP。
  model_validate 解析任意输入对象。
  三者不是同一个东西。

[V32] Streaming
  文本 delta 可展示。结构化 JSON 片段不能当完整对象。
  等流结束再读 final_output。不要每个 delta 都 validate。

[V33] Handoff
  Agent.handoffs / handoff() 把当前轮次交给另一个 Agent。
  模型选择 transfer_to_*，不是 Python if/else。
  交接后目标 Agent 生成最终回答。result.last_agent 是本轮回答者。

[V33] input_type / on_handoff
  input_type 是交接 Tool 的 Pydantic 元数据，不替换下一位 Agent 的用户输入。
  提供 input_type 必须同时给 on_handoff。
  鉴权、user_id、AsyncSession 仍来自 AgentContext。

[V33] Agents as Tools
  Agent.as_tool() 让 Manager 调用专家子任务，控制权不交出去。
  专家拿到生成的 input，结果回到 Manager。last_agent 仍是 Manager。

[V33] 下一轮入口
  SDK Session 不会自动选择下一轮 Agent。
  本版每个 HTTP 请求都从 Triage 开始。

[V34] Input Guardrail
  链首 Agent 运行前检查输入。run_in_parallel=False 才会阻塞 Tool。
  tripwire_triggered=True 抛 InputGuardrailTripwireTriggered。
  不是普通 Tool，也不是 LLM 分类器权限系统。

[V34] Output Guardrail
  最终输出已经生成后才检查。不等于 Pydantic response_model。
  追不回已经通过 SSE 发出的 delta。

[V34] Tool Guardrail
  Input 在 Tool 前；Output 在 Tool 后，不能撤销已执行的数据库操作。
  allow / reject_content / raise_exception 三条路。

[V34] 异常映射
  SDK Exception → AgentRunError → HTTP/SSE。应用层 code 不是 SDK 字段。
  max_turns 是 Agent Loop 轮次，不是历史条数。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
