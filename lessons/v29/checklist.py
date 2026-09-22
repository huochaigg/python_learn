"""
文件作用：V29 自测题。只问不答。
运行命令：uv run python lessons/v29/checklist.py
观察重点：能从 FastAPI 请求追到 MySQL 再回到 Agent Response。
"""

CHECKLIST = [
    "能解释 Agent 是什么",
    "能解释 Agent 和 Runner 区别",
    "能解释 Runner.run 为什么 await",
    "能解释 Runner.run 为什么不一定只有一次模型调用",
    "能解释 Agent Loop",
    "能解释 Function Tool 工作流程",
    "能解释参数类型为什么重要",
    "能解释 Tool Schema 从哪里来",
    "能解释 Tool 到底是谁执行的",
    "能解释 RunResult",
    "能解释 final_output",
    "能解释 RunContextWrapper",
    "能区分 Local Context 与 LLM Context",
    "能解释 Agent[Context] 泛型",
    "能写 async function tool",
    "能把 FastAPI request-scoped AsyncSession 传给 Tool",
    "知道不能让全局 Agent 持有 AsyncSession",
    "知道同一个 AsyncSession 不适合多个并发 Task 共享",
    "能解释 Router / Service / Agent / Tool / Repository 分层",
    "能从 FastAPI 请求追踪到 MySQL 再回到 Agent Response",
]


def main() -> None:
    print("===== V29 checklist（先自己答）=====")
    for index, item in enumerate(CHECKLIST, start=1):
        print()
        print(f"{index}. {item}")
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v29 checklist 运行完毕 ---")
