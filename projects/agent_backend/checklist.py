"""
文件作用：长期自测题索引。
运行命令：uv run python projects/agent_backend/checklist.py
"""

CHECKLIST = [
    "[V31] 能解释 SDK Session 与 AsyncSession 的区别",
    "[V31] 能通过 conversation_id 完成多轮对话",
    "[V32] 知道 Agent.output_type 做什么",
    "[V32] 能解释为什么 final_output 可以是 Pydantic 对象",
    "[V32] 能区分 Tool Result 和 Agent Final Output",
    "[V32] 能写出 Field / Literal 校验",
    "[V32] 能区分 Pydantic 错误、SDK Structured Output 错误、业务库存错误",
    "[V32] 能解释 output_type 与 FastAPI response_model 的区别",
    "[V32] 知道不要对每个 SSE delta 做完整 JSON 校验",
    "[V32] 知道 can_purchase 必须基于库存规则而不是模型权限幻觉",
    "[V32] 商品不存在时不会用 stock=0 伪装",
    "[V32] 旧版 /agent/chat 仍返回普通文本",
    "[V33] 能解释 Handoff 与 Function Tool 的区别",
    "[V33] 能解释 Handoff 与 Agents as Tools 的区别",
    "[V33] 知道 on_handoff 何时执行",
    "[V33] 知道 input_type 不替代用户输入和 AgentContext",
    "[V33] 知道 result.last_agent 不是下一轮 HTTP 入口",
    "[V33] 能说明 RECOMMENDED_PROMPT_PREFIX 解决什么问题",
    "[V33] 库存请求应交给 Inventory Agent",
    "[V33] 订单请求应交给 Order Agent",
    "[V33] Manager 调用专家后仍自己生成最终回答",
]


def main() -> None:
    print("===== agent_backend checklist =====")
    for index, item in enumerate(CHECKLIST, start=1):
        print()
        print(f"{index}. {item}")
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- checklist 运行完毕 ---")
