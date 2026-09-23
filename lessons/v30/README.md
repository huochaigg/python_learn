# v30 OpenAI Agents SDK Streaming + FastAPI SSE

V29 已经会 `Runner.run` + Function Tool + AsyncSession。本版只加一条链路：

`Runner.run_streamed()` → `stream_events()` → SSE → `fetch` ReadableStream。

## 学习目标

搞懂 SDK Streaming 和 SSE 不是一回事，以及如何把文本 delta、Tool 事件安全地推到浏览器。

## 前置知识

V29：Agent、Runner.run、Function Tool、RunContextWrapper、FastAPI、AsyncSession、真实 MySQL 库存查询。

## 学习顺序

1. `01_basic_stream_demo.py`
2. `02_tool_stream_demo.py`
3. `03_sse_format_demo.py`
4. `app/core/sse.py` → `encode_sse()`
5. `app/services/agent_service.py` → `stream_chat()`
6. `app/routers/agent_router.py` → `stream_chat()`
7. `frontend/index.html`
8. 浏览器完整跑一次
9. `notes.py` / `checklist.py` / `concept_index.py`

## 项目结构

在 V29 app 结构上增量：

- 新增 `app/core/sse.py`、`app/services/stream_events.py`
- 新增 `frontend/index.html`
- 修改 `agent_service.py`、`agent_router.py`、`main.py`

## 新增/修改文件

新增：三个 demo、`sse.py`、`stream_events.py`、`frontend/index.html`、本 README。

修改：`AgentService.stream_chat()`、`POST /agent/chat/stream`、`main.py` 提供首页和 CORS。

V29 保持不变。

## 环境变量

复制 `lessons/v30/.env.example` 为 `lessons/v30/.env`。独立库 `python_learn_v30`，避免覆盖 V29。

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=python_learn_v30
```

## 数据库初始化

```sql
CREATE DATABASE python_learn_v30 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```
uv run python lessons/v30/init_db.py
```

## 三个 Demo 运行命令

```
uv run python lessons/v30/01_basic_stream_demo.py
uv run python lessons/v30/02_tool_stream_demo.py
uv run python lessons/v30/03_sse_format_demo.py
```

## FastAPI 启动命令

```
uv run fastapi dev lessons/v30/app/main.py --port 8001
```

浏览器打开：

```
http://127.0.0.1:8001/
```

同一端口提供 HTML，默认不需要跨域。若用 `file://` 打开 HTML，才需要 CORS（本版已允许 `*`）。不要把 EventSource 和 fetch 当成同一个 API：EventSource 适合 GET SSE；本版聊天是 POST JSON，所以用 fetch 读 SSE。

## curl -N 测试命令

`-N` 关闭缓冲，才能看到流。

```
curl -N -X POST http://127.0.0.1:8001/agent/chat/stream -H "Content-Type: application/json" -d "{\"message\":\"SKU002 还有多少库存？\"}"
```

## SSE 协议

```
event: delta
data: {"content":"你好"}

```

`event:` 事件名；`data:` JSON 载荷；可选 `id:` / `retry:`。两个换行结束当前事件。

SSE 是 HTTP 响应流的文本协议，不是 WebSocket，也不是 SDK Streaming。

## 完整请求流程

```
HTTP POST /agent/chat/stream
→ Router StreamingResponse
→ async with AsyncSessionLocal()
→ AgentService.stream_chat()
→ Runner.run_streamed()
→ async for stream_events()
→ encode_sse()
→ 浏览器 fetch ReadableStream
```

## SDK Streaming 与 SSE 的区别

SDK Streaming：服务端内部的 Agent 事件（delta、tool item）。

SSE：把**应用层**事件发给浏览器。不要把全部原始 SDK 事件转发到前端。

## Tool Event 流程

模型决定调 Tool → `tool_call_item` → Python `get_product_stock` 查 MySQL → `tool_call_output_item` → 模型继续生成文本 delta → `is_complete` 后应用层 `event: done`。

不要把 `message_output_item` 的完整文本再拼到已经发送的 delta 后面。

## AsyncSession 生命周期

`StreamingResponse` 返回后，响应内容还在生成。V29 的 `Depends(get_db)` 适合一次性 JSON。本版在 generator 里 `async with AsyncSessionLocal()`，保证 Tool 查库时 Session 仍有效。

Agent 仍是模块级配置，不持有 Session。不要把同一个 Session 给多个并发 Task。

## 取消和错误处理

前端 `AbortController.abort()` 只取消 HTTP。不等于 Agent 成功完成，也不等于数据库 rollback。本版 Tool 只读库存。

`result.cancel()` 后必须继续消费 `stream_events()` 做清理。

流开始前可以 HTTP 500；流开始后只能 `event: error`。不要把堆栈发给前端。

最后一个 delta ≠ Run 完成。消费完流再检查 `is_complete`，再发 `done`。`done` 是应用协议，不是 SDK 自动事件。

## 本版本概念定位

- Runner.run_streamed → `01_basic_stream_demo.py` → `main()`；`AgentService.stream_chat()`
- ResponseTextDeltaEvent → `01_basic_stream_demo.py` → `main()`；`extract_text_delta()`
- Tool StreamEvent → `02_tool_stream_demo.py` → `main()`
- SSE Formatter → `app/core/sse.py` → `encode_sse()`
- StreamingResponse → `app/routers/agent_router.py` → `stream_chat()`
- fetch ReadableStream → `frontend/index.html` → `sendMessage()`
- AbortController → `frontend/index.html` → `stopMessage()`

## V29 与 V30 的区别

V29：`await Runner.run()`，一次性 JSON。

V30：`Runner.run_streamed()` + SSE，边生成边推送，并正确保住流式过程中的 AsyncSession。
