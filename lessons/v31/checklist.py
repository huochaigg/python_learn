"""
文件作用：V31 自测题。只问不答。
运行命令：uv run python lessons/v31/checklist.py
观察重点：能从 session_id 追到 MySQL 历史，再追到业务 Message。
"""

CHECKLIST = [
    "知道 SDK Session 的作用",
    "能解释 session_id",
    "能解释 Session 与 AsyncSession 的区别",
    "能解释 AgentContext 与 Conversation History 的区别",
    "知道 SDK 如何读取历史",
    "知道 SDK 如何保存历史",
    "知道为什么不能重复拼接 messages",
    "能理解 SQLAlchemySession",
    "能通过真实 MySQL 恢复历史",
    "能实现多个 Conversation 隔离",
    "能区分 SDK 历史与业务 Message",
    "能理解一次 Agent Run 与一次 Conversation 的关系",
    "能理解流式消息的保存时机",
    "知道不能每个 delta 都 commit",
    "能解释同会话并发问题",
    "知道 asyncio.Lock 的适用范围",
    "能解释 SDK 历史与业务表不一定原子化",
    "能通过 conversation_id 完成多轮对话",
]


def main() -> None:
    print("===== V31 checklist（先自己答）=====")
    for index, item in enumerate(CHECKLIST, start=1):
        print()
        print(f"{index}. {item}")
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v31 checklist 运行完毕 ---")
