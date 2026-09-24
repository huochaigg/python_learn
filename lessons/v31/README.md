# v31 OpenAI Agents SDK Session + MySQL 会话历史

V30 已经会流式 Agent。本版只加多轮对话和持久化：同一 `conversation_id` 跨请求、跨进程仍能接着聊。

## 版本目标

让真实 Agent 后端支持多轮对话、多个独立会话、MySQL 持久化、历史查询，以及服务重启后恢复上下文。

## 前置知识

V30：FastAPI、AsyncSession、Runner.run / run_streamed、Function Tool、SSE。本版不再重讲这些。

## 目录结构

在 V30 app 上增量：新增 `models/conversation.py`、`models/message.py`、`sessions/`、会话 Router；`AgentService` 增加 `session=`。

## 三个 Demo 的学习顺序

1. `01_sqlite_session_demo.py`
2. `02_sqlalchemy_session_demo.py`
3. `03_session_isolation_demo.py`
4. Conversation / Message ORM
5. `get_agent_session()`
6. `AgentService.chat()` / `stream_chat()`
7. Router 接口
8. 前端会话列表
9. 完整多轮对话
10. `notes.py` / `checklist.py` / `concept_index.py`

## 新增和修改的文件

新增：三个 Demo、`sessions/`、Conversation/Message、会话 CRUD、本 README。

修改：`AgentService` 传入 SDK Session 并写业务消息；聊天请求增加 `conversation_id`；前端增加会话列表。

V30 保持不变。

## 环境变量

复制 `lessons/v31/.env.example` 为 `lessons/v31/.env`。独立库 `python_learn_v31`。

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=python_learn_v31
```

## MySQL 初始化

```sql
CREATE DATABASE python_learn_v31 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```
uv run python lessons/v31/init_db.py
```

SDK `SQLAlchemySession` 复用现有 `mysql+asyncmy` AsyncEngine，不退回同步 pymysql。当前 openai-agents 0.22.3 的构造是 `SQLAlchemySession(session_id, engine=engine, create_tables=False)`。

官方 `create_tables=True` 在 MySQL 上会因为 `String` 没有长度编译失败。本版用兼容 DDL 创建同样的 `agent_sessions` / `agent_messages`（只补 VARCHAR 长度），不改 SDK 内部代码，也不改表语义。

## 运行命令

```
uv run python lessons/v31/01_sqlite_session_demo.py
uv run python lessons/v31/02_sqlalchemy_session_demo.py
uv run python lessons/v31/03_session_isolation_demo.py
uv run fastapi dev lessons/v31/app/main.py --port 8001
```

浏览器：`http://127.0.0.1:8001/`

本地开发固定 `X-User-Id: 1`。这不是认证系统；接口仍校验会话归属。

## 接口调用

```
curl -X POST http://127.0.0.1:8001/conversations -H "Content-Type: application/json" -H "X-User-Id: 1" -d "{\"title\":\"库存会话\"}"

curl -X POST http://127.0.0.1:8001/agent/chat -H "Content-Type: application/json" -H "X-User-Id: 1" -d "{\"conversation_id\":\"替换成真实id\",\"message\":\"SKU002 还有多少库存？\"}"

curl -N -X POST http://127.0.0.1:8001/agent/chat/stream -H "Content-Type: application/json" -H "X-User-Id: 1" -d "{\"conversation_id\":\"替换成真实id\",\"message\":\"我刚才问的是哪个 SKU？\"}"

curl http://127.0.0.1:8001/conversations/替换成真实id/messages -H "X-User-Id: 1"
```

## 本版本概念定位

- SQLAlchemySession → `02_sqlalchemy_session_demo.py` → `main()`；`get_agent_session()`
- Conversation → `app/models/conversation.py`
- Message → `app/models/message.py`
- Runner Session → `AgentService.chat()`
- 流式 Session → `AgentService.stream_chat()`
- 历史查询 → `list_messages()`
- 会话删除 → `ConversationService.delete()`

## 三种 Session / Context 区别

**Agent Session（SDK Session）**：模型对话上下文。按 `session_id` 加载/保存。本版 `session_id = conversation_id`。

**SQLAlchemy AsyncSession**：数据库工作单元。Tool 查库存、业务 Message 写入都用它，但是**短事务**，不是聊天历史对象。

**AgentContext**：本次 Agent Run 的本地依赖（`db`、`user_id`）。不会自动变成 prompt，更不是 Conversation History。

三者可以共用同一个 AsyncEngine，但不是同一个对象，也不共享同一个事务。

## 多轮对话数据流

第一次请求：

用户输入 → conversation_id → 校验归属 → 获取 SQLAlchemySession → SDK `get_items()` 为空 → Runner → Agent → Tool → 最终回答 → SDK `add_items()` → 业务 Message 保存 → 返回。

第二次请求：

同一个 conversation_id → 新的 SQLAlchemySession 对象（历史在 MySQL）→ `get_items()` 读出上一轮 → 新用户消息 → Runner → 保存新历史。

模型本身不会记住上一次 HTTP。是持久化历史让多轮成为可能。

不要手动查出旧消息再拼进 `Runner.run` 的 input，同时又传 `session=`。SDK 会自己加载历史，再拼一次会重复上下文。

## SDK 历史与业务消息区别

SDK 历史：给模型继续推理，可能包含 tool_call / tool_output 等结构化条目。存在 `agent_sessions` / `agent_messages`。

业务 Message：给前端展示、分页、状态（pending/completed/failed）。存在 `messages`。

一次 Agent Run 是 Conversation 里的一轮，不是整个 Conversation。

两套写入使用不同事务，不自动原子化。SDK 跑成功但业务 Message 保存失败时：打完整日志、接口报错、助手消息不能假装 completed。后续可以用对账/重试补写业务表，本版不实现分布式事务。

## 流式消息持久化

用户 Message 先写入 completed。助手 Message 先 pending。流式过程只在内存累加 delta，不每个 token commit。`is_complete` 后再把助手更新为 completed。客户端断开或 Run 失败更新为 failed，不得标 completed。HTTP 取消会取消当前 Task，本版会先写完 failed 再把 `CancelledError` 抛回去。

流式 HTTP 持续期间不长期占用一个业务事务。Tool 的 AsyncSession 与 Message 短事务分开。

## 会话并发

同一 `conversation_id` 同时发两条，两次 Run 可能读到同一份旧历史，写入顺序错乱。

本版用进程内 `ConversationRunGuard`：第二个活动请求返回 409。

`asyncio.Lock` 只在同一进程有效。多 Worker 要 Redis/数据库锁，本版不做。

## 事务边界

- SDK Session 内部自己 `begin()` 写历史。
- 业务 Message 每次 `async with AsyncSessionLocal()` 短事务提交。
- Tool 查询使用请求/流式 generator 内的另一个 AsyncSession。
- 删除会话：先 `clear_session()`，再删业务行。任一步失败不能返回删除成功。

## 真实项目意义

用户刷新页面、服务重启后，仍能按 Conversation 列表恢复展示，并让模型接着聊。这是聊天产品的基础，而不是把全部历史每次从浏览器再 POST 回去。

## V30 与 V31 的区别

V30：每次请求都是独立 Run，没有跨请求记忆。

V31：`Runner.run(..., session=session)`，MySQL 持久化，多会话隔离，业务消息可查询。
