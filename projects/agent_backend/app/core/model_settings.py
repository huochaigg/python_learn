from agents import ModelSettings

from .config import settings


def structured_output_model_settings() -> ModelSettings:
    # OpenAI 官方用 response_format.json_schema。
    # DeepSeek 等兼容网关会 400：This response_format type is unavailable now。
    # extra_body 覆盖为 json_object；SDK 仍用 output_type 在本地校验 JSON。
    if settings.openai_base_url:
        return ModelSettings(extra_body={"response_format": {"type": "json_object"}})
    return ModelSettings()
