"""
文件作用：V31 概念定位索引。
运行命令：uv run python lessons/v31/concept_index.py
观察重点：按概念找到文件 → 函数。
"""

CONCEPT_INDEX = {
    "SQLiteSession": [
        "01_sqlite_session_demo.py -> main()",
    ],
    "SQLAlchemySession": [
        "02_sqlalchemy_session_demo.py -> main()",
        "app/sessions/agent_session.py -> get_agent_session()",
    ],
    "session_id isolation": [
        "03_session_isolation_demo.py -> main()",
    ],
    "Conversation": [
        "app/models/conversation.py -> Conversation",
        "app/services/conversation_service.py -> ConversationService.create()",
    ],
    "Message": [
        "app/models/message.py -> Message",
        "app/repositories/message_repository.py -> list_by_conversation()",
    ],
    "Runner Session": [
        "app/services/agent_service.py -> AgentService.chat()",
    ],
    "stream Session": [
        "app/services/agent_service.py -> AgentService.stream_chat()",
    ],
    "history query": [
        "app/repositories/message_repository.py -> list_by_conversation()",
        "app/routers/conversation_router.py -> list_messages()",
    ],
    "session delete": [
        "app/services/conversation_service.py -> ConversationService.delete()",
        "app/routers/conversation_router.py -> delete_conversation()",
    ],
    "in-process lock": [
        "app/sessions/run_guard.py -> ConversationRunGuard.try_acquire()",
    ],
}


def main() -> None:
    print("===== V31 concept_index =====")
    for name, locs in CONCEPT_INDEX.items():
        print(name)
        for loc in locs:
            print(f"  {loc}")


if __name__ == "__main__":
    main()
