# Agent Backend

从 V32 起的长期演进项目。V1～V31 历史课仍在 `lessons/`。

当前版本：**V33 Handoff + Multi-Agent + Agents as Tools**。

详细记录：`docs/v33.md`。上一版：`docs/v32.md`。

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
