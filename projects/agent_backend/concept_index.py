"""
文件作用：长期概念定位。新增版本往字典里追加，不删旧键。
运行命令：uv run python projects/agent_backend/concept_index.py
"""

CONCEPT_INDEX = {
    "SQLAlchemySession": [
        "[V31] app/sessions/agent_session.py -> get_agent_session()",
    ],
    "Conversation": [
        "[V31] app/models/conversation.py -> Conversation",
    ],
    "Structured Output": [
        "[V32] demos/v32/01_structured_output_demo.py -> main()",
    ],
    "ProductAnalysis": [
        "[V32] app/schemas/product.py -> ProductAnalysis",
    ],
    "Agent.output_type": [
        "[V32] app/agents/product_analysis_agent.py -> product_analysis_agent",
    ],
    "ProductStockResult": [
        "[V32] app/schemas/product.py -> ProductStockResult",
        "[V32] demos/v32/02_tool_structured_demo.py -> main()",
    ],
    "Response DTO": [
        "[V32] app/schemas/product.py -> ProductAnalyzeResponse",
        "[V32] app/routers/agent_router.py -> analyze_product()",
    ],
    "Pydantic validation": [
        "[V32] demos/v32/03_validation_demo.py -> main()",
        "[V32] tests/test_v32_pydantic.py",
    ],
    "Handoff": [
        "[V33] app/agents/triage_agent.py -> triage_agent",
        "[V33] demos/v33/01_handoff_basic_demo.py -> main()",
    ],
    "handoff()": [
        "[V33] app/agents/triage_agent.py -> handoff()",
    ],
    "on_handoff": [
        "[V33] app/agents/triage_agent.py -> on_inventory_handoff()",
    ],
    "input_type": [
        "[V33] app/schemas/handoff.py -> HandoffData",
    ],
    "Agent.as_tool": [
        "[V33] app/agents/manager_agent.py -> manager_agent",
        "[V33] demos/v33/03_agents_as_tools_demo.py -> main()",
    ],
    "result.last_agent": [
        "[V33] app/agents/run_trace.py -> last_agent_name()",
    ],
    "Input Guardrail": [
        "[V34] demos/v34/01_input_guardrail_demo.py -> main()",
        "[V34] app/guardrails/input_guardrails.py -> check_business_scope()",
    ],
    "Output Guardrail": [
        "[V34] demos/v34/02_output_guardrail_demo.py -> main()",
        "[V34] app/guardrails/output_guardrails.py -> check_final_output()",
    ],
    "Tool Input Guardrail": [
        "[V34] demos/v34/03_tool_guardrail_demo.py -> main()",
        "[V34] app/guardrails/tool_guardrails.py -> check_sku_tool_input()",
    ],
    "Tool Output Guardrail": [
        "[V34] app/guardrails/tool_guardrails.py -> check_tool_output_secrets()",
    ],
    "Exception Mapping": [
        "[V34] app/core/agent_exceptions.py -> map_sdk_exception()",
    ],
}


def main() -> None:
    print("===== agent_backend concept_index =====")
    for name, locs in CONCEPT_INDEX.items():
        print(name)
        for loc in locs:
            print(f"  {loc}")


if __name__ == "__main__":
    main()
