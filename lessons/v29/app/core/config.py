from pathlib import Path

from agents import set_default_openai_api, set_default_openai_client, set_default_openai_key, set_tracing_disabled
from openai import AsyncOpenAI
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
    database_host: str = "127.0.0.1"
    database_port: int = 3306
    database_user: str = "root"
    database_password: str = ""
    database_name: str = "python_learn_v29"
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

# Agents SDK 默认读 OPENAI_API_KEY。Key 只来自 .env，不要写进代码。
# openai_base_url 留空走官方 OpenAI；填写时走 OpenAI 兼容网关，并用 chat_completions。
if settings.openai_api_key:
    if settings.openai_base_url:
        set_default_openai_client(
            AsyncOpenAI(api_key=settings.openai_api_key, base_url=settings.openai_base_url)
        )
        set_default_openai_api("chat_completions")
        set_tracing_disabled(True)
    else:
        set_default_openai_key(settings.openai_api_key)


def require_openai_key() -> None:
    if not settings.openai_api_key:
        raise SystemExit("缺少 OPENAI_API_KEY，请填写 lessons/v29/.env")
