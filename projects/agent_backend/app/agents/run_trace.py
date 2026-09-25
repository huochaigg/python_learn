from typing import Any


def last_agent_name(result: Any) -> str:
    # result.last_agent：本轮 Runner 结束时正在负责的 Agent。
    # Handoff 后通常是专家；as_tool 后通常仍是 Manager。不是下一轮 HTTP 的入口。
    agent = getattr(result, "last_agent", None)
    return getattr(agent, "name", "unknown")


def list_handoffs(result: Any) -> list[str]:
    records: list[str] = []
    for item in getattr(result, "new_items", []) or []:
        if getattr(item, "type", None) == "handoff_output_item":
            source = getattr(getattr(item, "source_agent", None), "name", "?")
            target = getattr(getattr(item, "target_agent", None), "name", "?")
            records.append(f"{source}->{target}")
    return records


def list_tool_names(result: Any) -> list[str]:
    names: list[str] = []
    for item in getattr(result, "new_items", []) or []:
        if getattr(item, "type", None) == "tool_call_item":
            names.append(getattr(item, "tool_name", None) or "tool")
    return names
