"""
文件作用：V29 概念定位索引。
运行命令：uv run python lessons/v29/concept_index.py
观察重点：按概念找到文件 → 类/函数。
"""

CONCEPT_INDEX = {
    "Agent": [
        "01_agent_basic_demo.py -> agent",
        "app/agents/product_agent.py -> product_agent",
    ],
    "Runner.run": [
        "01_agent_basic_demo.py -> main()",
        "app/services/agent_service.py -> AgentService.chat()",
    ],
    "RunResult / final_output": [
        "01_agent_basic_demo.py -> main()",
        "app/services/agent_service.py -> AgentService.chat()",
    ],
    "Function Tool": [
        "02_function_tool_demo.py -> get_product_stock()",
        "app/tools/product_tools.py -> get_product_stock()",
    ],
    "RunContextWrapper": [
        "03_async_tool_context_demo.py -> get_current_user_info()",
        "app/tools/product_tools.py -> get_product_stock()",
    ],
    "AgentContext": [
        "03_async_tool_context_demo.py -> AgentContext",
        "app/agents/context.py -> AgentContext",
    ],
    "AsyncSession in Agent Context": [
        "app/services/agent_service.py -> AgentService.chat()",
        "app/tools/product_tools.py -> get_product_stock()",
    ],
    "FastAPI Agent endpoint": [
        "app/routers/agent_router.py -> chat()",
    ],
    "Repository": [
        "app/repositories/product_repository.py -> ProductRepository.get_by_sku()",
    ],
}


def main() -> None:
    print("===== V29 concept_index =====")
    for name, locs in CONCEPT_INDEX.items():
        print(f"{name}")
        for loc in locs:
            print(f"  {loc}")


if __name__ == "__main__":
    main()
