# V35 Tracing + Agent Testing + Observability

长期项目 `projects/agent_backend/` 增量版本。不新建 `lessons/v35`。

## 学习目标

一次 Agent Run 内部到底发生了什么，以及 Agent / Tool / Handoff / Guardrail / Session 怎么做可靠测试。

本版 API：`trace()`、`custom_span()`、`workflow_name`、`trace_id`、`group_id`、`metadata`、`RunConfig` 里的 tracing 字段、官方 `agents.testing.ScriptedModel`。

不要在本版深入：自定义 Trace Processor、OpenTelemetry、Prometheus、Grafana。

## Trace 是什么

Trace ≈ 一次完整业务工作流。

例如：用户查询库存。一次 `Runner.run` / `Runner.run_streamed` 通常对应一次 Trace。

`trace()` 返回 Trace 对象。要用 context manager：

```python
with trace("inventory-agent-workflow", group_id=conversation_id, metadata={...}):
    result = await Runner.run(...)
```

进入时 start，离开时 finish。异常也会结束 Trace，所以失败请求同样能被看到。

## Span 是什么

Span ≈ 这个工作流中的一个步骤。

常见自动 Span（不必背全）：

- Agent
- Generation
- Function Tool
- Guardrail
- Handoff

父子关系描述「先生成、再调 Tool、再生成」。耗时也在 Span 上。

## Trace vs Logging

| | Logging | Tracing |
|---|---|---|
| 谁写 | 程序主动 `logger.info` / `logger.error` | SDK / `trace()` / `custom_span()` 记录步骤关系 |
| 内容 | 一行事件 | 一次请求内部的树状步骤 + 耗时 |
| 替代？ | 否 | 否 |

生产环境通常两个都要。日志方便搜错误；Trace 方便看这一次 Run 卡在哪一步。

出现线上错误时，至少希望能对上：

- HTTP `request_id`（本项目尚未单独实现，概念上要有）
- `trace_id`：这一次 workflow
- `conversation_id`：这个业务会话

`AgentService.chat()` / `stream_chat()` 把 `trace_id` 放进 `logger.info(..., extra={"trace_id": ...})`。这是关联方式，不是把 Trace 当业务数据库。

## 四个 ID 不要混

| 名字 | 是什么 |
|---|---|
| `conversation_id` | 业务会话 ID |
| `session_id` | Agent 历史上下文标识（本项目里常等于 conversation_id） |
| `trace_id` | 一次具体 Run / Workflow 的追踪 ID |
| `group_id` | 把多个相关 Trace 归为一组 |

`conversation_id` 适合当 `group_id`：同一对话的多次 Agent Run 可以按组查看。

## metadata

可以放：`user_id`、`conversation_id`、`agent_name`、`environment`。

不要放：API Key、密码、Token、完整敏感业务数据。

metadata 用来搜索和排查，不是业务表。

## 自动 Tracing

Agents SDK 默认已经对 `Runner.run` / `Runner.run_streamed` 做 tracing。

因此：**不是每个 Tool 都需要手写 `custom_span`。**

本项目若配置了兼容网关 `OPENAI_BASE_URL`，会 `set_tracing_disabled(True)`，因为没有 OpenAI Tracing Dashboard。本地 `trace()` 仍可进入 context；`get_current_trace()` 可能返回 `trace_id=no-op`，只是默认不上报到 platform.openai.com。

## custom_span

只在 SDK 自动 Trace 覆盖不到、又真正有业务观察价值时使用。例如：

- 数据库复杂业务处理
- 自定义 RAG Pipeline
- 外部 API 调用
- 复杂订单计算

反例：给 `get_product_stock` 再包一层同名 Span。

## 失败追踪

Tool 抛异常、Guardrail tripwire、Agent Run 失败时，已经发生的步骤仍应留在 Trace 里。

Tracing 不只是看成功请求。线上更常查失败请求。

## 隐私

Trace 可能包含 Prompt、Tool 输入输出、模型输出。

不要把密码、Token、API Key、高敏感个人信息写入 metadata 或 Span data。

生产环境还要考虑脱敏、保留策略、是否关闭敏感数据追踪。本版只理解原则。

## 测试策略

Agent 测试不能全部依赖真实模型 API：不稳定、慢、花钱、易受模型版本影响。

两层：

1. **确定性测试**：`ScriptedModel`。验证 Tool 是否被调用、Handoff 是否发生、Guardrail 是否触发、Session 是否写入。
2. **少量 Integration Test**：真实调用模型，验证整条链路能跑通。本项目已有 `test_v32_agent_api.py`、`test_v33_agent_api.py`、`test_v34_agent_api.py`、MySQL 测试。V35 不再新增真实模型测试。

### ScriptedModel

官方 `agents.testing.ScriptedModel`。按预先写好的步骤返回 `function_call` / `assistant_message`，或抛异常。

确定性：步骤是代码写死的。不会请求真实模型。

适合：Agent orchestration、Tool call、Handoff、Guardrail、Session。

不适合：真实模型理解能力、Prompt 好不好、输出质量。不要自己写 FakeModel 冒充这套 API。

### Unit / Integration / E2E

| 类型 | 在本项目里测什么 | 例子 |
|---|---|---|
| Unit | Tool / Service / Guardrail / Agent orchestration | `test_agent_basic.py`、`test_tool_call.py`、`test_handoff.py`、`test_guardrail.py`、`test_session.py`、`test_guardrails.py` |
| Integration | Agent + SDK + MySQL + Session | `test_v32_agent_api.py`、`test_v33_mysql.py`、`test_v33_agent_api.py`、`test_v34_agent_api.py` |
| E2E | FastAPI → Agent → Tool → Database → Response | 浏览器走 `http://127.0.0.1:8001/`，或带 Key 的 API 测试 |

不要强行让所有测试都成为 E2E。

### Agent 测试原则

- 不测 LLM 智商，测编排。
- Tool 测试记录 `tool_called` / `tool_args` / `tool_result`（本项目用 `context.tool_calls` + Repository mock）。
- Handoff 测 `last_agent` 和 `handoff_output_item`，不要靠最终字符串猜。
- Guardrail 测异常类型，并且确认阻塞模式下 Tool 没执行。
- Session 单测用 `SQLiteSession`，MySQL 留给 integration。

## FastAPI 整合

`AgentService.chat()` / `stream_chat()` 用 `conversation_id` 作为 `group_id` 打开 `trace()`。没有重构整个项目。

## 本版本文件定位

- Demo：`demos/v35/04_tracing_demo.py`、`demos/v35/05_custom_span_demo.py`
- 测试：`tests/test_agent_basic.py`、`test_tool_call.py`、`test_handoff.py`、`test_guardrail.py`、`test_session.py`
- 辅助：`app/core/tracing.py`、`tests/scripted_support.py`

## 运行

```
uv run python projects/agent_backend/demos/v35/04_tracing_demo.py
uv run python projects/agent_backend/demos/v35/05_custom_span_demo.py
uv run pytest
uv run fastapi dev projects/agent_backend/app/main.py --port 8001
```
