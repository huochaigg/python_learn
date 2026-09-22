from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "python_learn_v28"
    db_charset: str = "utf8mb4"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    @property
    def database_url(self) -> URL:
        # mysql+asyncmy：mysql 是 SQLAlchemy dialect；asyncmy 是支持 asyncio 的 MySQL driver。
        # 同步 PyMySQL 不能直接让 AsyncEngine 获得真正异步 DB IO。
        return URL.create(
            drivername="mysql+asyncmy",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": self.db_charset},
        )


settings = Settings()
