from agents import gen_trace_id, get_current_trace, trace


def agent_trace_metadata(
    *,
    user_id: int,
    conversation_id: str,
    agent_name: str,
    environment: str = "local",
) -> dict[str, str]:
    # metadata 只给排查用：按 conversation/user/agent 过滤 Trace。
    # 不要放 API Key、密码、Token、完整用户消息或库存敏感明细。
    return {
        "user_id": str(user_id),
        "conversation_id": conversation_id,
        "agent_name": agent_name,
        "environment": environment,
    }


def start_agent_trace(
    workflow_name: str,
    *,
    conversation_id: str,
    user_id: int,
    agent_name: str,
):
    # trace()：一次完整业务工作流。context manager 保证异常时也会 finish。
    # group_id 用 conversation_id，把同一会话的多次 Run 归到一组。
    # trace_id 是这一次 Run 的 ID，和 session_id / conversation_id 不是同一个东西。
    return trace(
        workflow_name,
        trace_id=gen_trace_id(),
        group_id=conversation_id,
        metadata=agent_trace_metadata(
            user_id=user_id,
            conversation_id=conversation_id,
            agent_name=agent_name,
        ),
    )


def current_trace_id() -> str | None:
    current = get_current_trace()
    return None if current is None else current.trace_id
