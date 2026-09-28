# Agent Backend

从 V32 起的长期演进项目。V1～V31 历史课仍在 `lessons/`。

当前版本：**V35 Tracing + Agent Testing + Observability**。

详细记录：`docs/v35_tracing_testing.md`。上一版：`docs/v34.md`。

## 启动

复制 `.env.example` 为 `.env`。独立库 `python_learn_agent`。

```sql
CREATE DATABASE python_learn_agent CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```
uv run python projects/agent_backend/init_db.py
uv run fastapi dev projects/agent_backend/app/main.py --port 8001
```

浏览器：`http://127.0.0.1:8001/`

## 隐私

Tracing 可能包含 Prompt、Tool 输入输出、模型输出。不要把密码、Token、API Key、高敏感个人信息写入 `trace()` metadata 或 `custom_span` data。生产环境还需要考虑脱敏和保留策略。

Agents SDK 默认已经对 `Runner.run` / `Runner.run_streamed` 做 tracing。不是每个 Tool 都要手写 `custom_span`。

本项目若使用兼容网关（`OPENAI_BASE_URL`），会关闭上报到 OpenAI Tracing Dashboard；本地仍用 `trace()` 给每次 Run 分配 `trace_id`，并用 `conversation_id` 作为 `group_id`。

## V35 Demo

```
uv run python projects/agent_backend/demos/v35/04_tracing_demo.py
uv run python projects/agent_backend/demos/v35/05_custom_span_demo.py
```

确定性测试（不请求真实模型）：

```
uv run pytest projects/agent_backend/tests/test_agent_basic.py projects/agent_backend/tests/test_tool_call.py projects/agent_backend/tests/test_handoff.py projects/agent_backend/tests/test_guardrail.py projects/agent_backend/tests/test_session.py
```

## V34 Demo

```
uv run python projects/agent_backend/demos/v34/01_input_guardrail_demo.py
uv run python projects/agent_backend/demos/v34/02_output_guardrail_demo.py
uv run python projects/agent_backend/demos/v34/03_tool_guardrail_demo.py
uv run python projects/agent_backend/demos/v34/04_agent_error_demo.py
```

## V33 Demo

```
uv run python projects/agent_backend/demos/v33/01_handoff_basic_demo.py
uv run python projects/agent_backend/demos/v33/02_handoff_context_demo.py
uv run python projects/agent_backend/demos/v33/03_agents_as_tools_demo.py
```

## V32 Demo

```
uv run python projects/agent_backend/demos/v32/01_structured_output_demo.py
uv run python projects/agent_backend/demos/v32/02_tool_structured_demo.py
uv run python projects/agent_backend/demos/v32/03_validation_demo.py
```

## 测试

```
uv run pytest projects/agent_backend/tests/test_v32_pydantic.py
uv run pytest projects/agent_backend/tests
```

没有 API Key 时，依赖模型的测试会 skip，不要改成假成功。

## 后续版本

直接在本目录增量改 `app/`，新实验放 `demos/vxx/`，知识放 `docs/vxx.md`。不要再复制整套项目。
