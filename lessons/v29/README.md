# v29 OpenAI Agents SDK 入门

V28 已经会 FastAPI + AsyncSession + MySQL。本版不再重讲那些基础，只把第一条 Agent 链路跑通。

## 推荐学习顺序

1. `01_agent_basic_demo.py`
2. `02_function_tool_demo.py`
3. `03_async_tool_context_demo.py`
4. `app/agents/product_agent.py`
5. `app/tools/product_tools.py`
6. `app/services/agent_service.py`
7. `app/routers/agent_router.py`
8. 从接口完整跑一次
9. `notes.py`
10. `checklist.py`
11. `concept_index.py`

## 学习目标

搞懂：

用户请求 → FastAPI Router → Service → Agent → `Runner.run()` → 模型是否调用 Function Tool → Tool 执行 → Tool Result 回 Agent Loop → `RunResult.final_output` → FastAPI Response。

## 前置知识

V27 Settings / MySQL，V28 `AsyncSession` + `asyncmy`。不要把同一个 `AsyncSession` 共享给多个并发 Task。

## 目录结构

```
lessons/v29/
├── README.md
├── notes.py
├── checklist.py
├── concept_index.py
├── 01_agent_basic_demo.py
├── 02_function_tool_demo.py
├── 03_async_tool_context_demo.py
├── init_db.py
└── app/
    ├── main.py
    ├── core/config.py
    ├── core/database.py
    ├── models/product.py
    ├── schemas/agent.py
    ├── repositories/product_repository.py
    ├── tools/product_tools.py
    ├── agents/context.py
    ├── agents/product_agent.py
    ├── services/agent_service.py
    └── routers/agent_router.py
```

## 环境变量

复制 `lessons/v29/.env.example` 为 `lessons/v29/.env`。不要提交真实 `.env`，不要把 API Key 写进代码。

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
# 走官方 OpenAI 时留空。OpenAI 兼容网关可填 base URL。
OPENAI_BASE_URL=
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=python_learn_v29
```

## 安装命令

```
uv add openai-agents
```

本仓库已加入 `openai-agents`。FastAPI / SQLAlchemy / asyncmy 沿用 V28。

## MySQL 初始化说明

独立库，避免覆盖 V27/V28：

```sql
CREATE DATABASE python_learn_v29 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

然后：

```
uv run python lessons/v29/init_db.py
```

幂等写入：

- SKU001 机械键盘 100
- SKU002 显示器 8
- SKU003 显卡 0

FastAPI 启动时也会 `create_all` + seed，不会重复插入同一 SKU。

## 运行三个 demo

```
uv run python lessons/v29/01_agent_basic_demo.py
uv run python lessons/v29/02_function_tool_demo.py
uv run python lessons/v29/03_async_tool_context_demo.py
```

```
uv run python lessons/v29/notes.py
uv run python lessons/v29/checklist.py
uv run python lessons/v29/concept_index.py
```

## 运行 FastAPI

```
uv run fastapi dev lessons/v29/app/main.py --port 8001
```

等价：

```
uv run uvicorn lessons.v29.app.main:app --reload --port 8001
```

## 接口调用示例

PowerShell：

```
uv run python -c "import requests; print(requests.post('http://127.0.0.1:8001/agent/chat', json={'message':'SKU002 还有多少库存？'}).text)"
```

curl：

```
curl -X POST http://127.0.0.1:8001/agent/chat -H "Content-Type: application/json" -d "{\"message\":\"SKU002 还有多少库存？\"}"
```

预期流程：模型调用 `get_product_stock` → Tool 查 MySQL 得到 8 → 自然语言回答库存。最终措辞不固定，但 Tool 查到的 stock 必须是数据库里的 8。

## 核心请求流程

```
HTTP Request
→ FastAPI Depends(get_db)
→ AsyncSession
→ AgentService
→ AgentContext(db=session)
→ Runner.run(...)
→ Agent
→ Tool
→ ctx.context.db
→ Repository
→ MySQL
→ Tool Result
→ Agent
→ RunResult
→ Response
→ get_db finally close
```

`Runner.run()` 必须在 `get_db()` 的 Session 仍然存活期间完成。

## Agent Loop

第一次模型调用：User Input + instructions + Tools Schema → Model。

- 直接回答 → `final_output` → `RunResult`
- 要调 Tool → Runner 识别 Tool Call → 校验参数 → 调用真实 Python 函数 → Tool Output 加入本次 run → 再次调用 Model → 继续调 Tool 或结束

`Runner.run()` ≠ 一次 OpenAI HTTP 请求。内部可能是 Model → Tool → Model → Tool → Model。

本版只使用 `Runner.run()`。`run_sync()` 给同步代码；`run_streamed()` 留给后续 SSE。

## 职责边界

| 层 | 职责 |
| --- | --- |
| Agent | 可复用的行为配置。不要持有 AsyncSession |
| Runner | runtime，执行 Agent Loop |
| Tool | 窄业务能力，例如 `get_product_stock(sku)`，不要 `execute_sql` |
| Service | 组装 Context、调用 `Runner.run`、取出 `final_output` |
| Repository | `select(Product)` |
| Router | HTTP |

窄 Tool 比万能 SQL Tool 更安全：参数可校验、权限边界清晰、模型不能乱写 SQL。

## 本版本概念定位

- Agent → `01_agent_basic_demo.py` → `agent`；`app/agents/product_agent.py` → `product_agent`
- Runner.run → `01_agent_basic_demo.py` → `main()`；`app/services/agent_service.py` → `AgentService.chat()`
- RunResult / final_output → `01_agent_basic_demo.py`；`AgentService.chat()`
- Function Tool → `02_function_tool_demo.py` → `get_product_stock()`；`app/tools/product_tools.py` → `get_product_stock()`
- RunContextWrapper → `03_async_tool_context_demo.py` → `get_current_user_info()`；`app/tools/product_tools.py` → `get_product_stock()`
- AgentContext → `03_async_tool_context_demo.py`；`app/agents/context.py`
- AsyncSession + Tool → `AgentService.chat()`；`get_product_stock()`
- FastAPI Agent endpoint → `app/routers/agent_router.py` → `chat()`
- Repository → `app/repositories/product_repository.py` → `get_by_sku()`

## 本版本暂不学习

Streaming、`Runner.run_streamed()`、SSE、Session / SQLiteSession、聊天历史、Structured Output、Handoff、Multi-Agent、Guardrails、Tracing 深入、RAG、Vector DB、MCP、Redis、队列、后台 Agent Run。
