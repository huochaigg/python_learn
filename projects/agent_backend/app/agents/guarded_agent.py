from agents import RunConfig

from ..guardrails.input_guardrails import check_business_scope
from ..guardrails.output_guardrails import check_final_output
from .triage_agent import triage_agent

# Input Guardrail 只挂在链首 Triage。Handoff 之后不会自动再跑一遍。
# Output Guardrail 通过 RunConfig 作用在整次 Run 的最终输出上。
# 每次 Tool 调用的校验在 Tool Guardrail / Repository，不在这里。
guarded_triage_agent = triage_agent.clone(
    name="Guarded Triage Agent",
    input_guardrails=[check_business_scope],
)

GUARDED_RUN_CONFIG = RunConfig(
    output_guardrails=[check_final_output],
)

GUARDED_MAX_TURNS = 8
