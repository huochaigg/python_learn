from pathlib import Path
import os

from agents import (
    set_default_openai_api,
    set_default_openai_client,
    set_default_openai_key,
    set_tracing_disabled,
    set_tracing_export_api_key,
)
from openai import AsyncOpenAI
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = ""
    # Tracing Dashboard 必须用 OpenAI 平台 Key。SDK 没有 OPENAI_AGENTS_KEY 这个官方变量。
    # 模型走 DeepSeek 时，OPENAI_API_KEY 不能用来上报 traces.ingest。
    openai_tracing_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("OPENAI_TRACING_API_KEY", "OPENAI_AGENTS_KEY"),
    )
    database_host: str = "127.0.0.1"
    database_port: int = 3306
    database_user: str = "root"
    database_password: str = ""
    database_name: str = "python_learn_agent"
    # 本地开发固定用户。这不是认证系统，只是为了练习会话归属校验。
    dev_user_id: int = 1
    database_charset: str = "utf8mb4"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    @property
    def database_url(self) -> URL:
        return URL.create(
            drivername="mysql+asyncmy",
            username=self.database_user,
            password=self.database_password,
            host=self.database_host,
            port=self.database_port,
            database=self.database_name,
            query={"charset": self.database_charset},
        )


settings = Settings()


def _under_pytest() -> bool:
    return "PYTEST_VERSION" in os.environ


def configure_model_and_tracing() -> None:
    # 模型客户端和 Tracing 导出是两套凭证：
    # OPENAI_API_KEY (+ BASE_URL) → 调 DeepSeek / 兼容网关
    # OPENAI_TRACING_API_KEY → set_tracing_export_api_key() → platform.openai.com/traces
    # pytest 里关闭上报，避免单测把脚本对话打到 Dashboard。
    if settings.openai_api_key:
        if settings.openai_base_url:
            set_default_openai_client(
                AsyncOpenAI(
                    api_key=settings.openai_api_key,
                    base_url=settings.openai_base_url,
                )
            )
            set_default_openai_api("chat_completions")
        else:
            set_default_openai_key(settings.openai_api_key)

    if _under_pytest():
        set_tracing_disabled(True)
        return
    if settings.openai_tracing_api_key:
        set_tracing_export_api_key(settings.openai_tracing_api_key)
        set_tracing_disabled(False)
        _tune_tracing_http_client()
        return
    set_tracing_disabled(True)


def _tune_tracing_http_client() -> None:
    # SDK 默认 connect timeout=5s。上报地址是 api.openai.com，不是 DeepSeek。
    # trust_env=True 会走系统 HTTP(S)_PROXY；国内直连超时是网络问题，不是变量名问题。
    import httpx2
    from agents.tracing.processors import default_exporter

    exporter = default_exporter()
    old = getattr(exporter, "_client", None)
    if old is not None:
        try:
            old.close()
        except Exception:
            pass
    exporter._client = httpx2.Client(
        timeout=httpx2.Timeout(timeout=60.0, connect=20.0),
        trust_env=True,
    )


configure_model_and_tracing()


def require_openai_key() -> None:
    if not settings.openai_api_key:
        raise SystemExit("缺少 OPENAI_API_KEY，请填写 projects/agent_backend/.env")
