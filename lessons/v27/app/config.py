from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

# Path(__file__)：按本文件位置找 lessons/v27/.env，不依赖启动时的当前工作目录。
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


class Settings(BaseSettings):
    # BaseSettings：专门从环境变量 / .env 加载配置，并按 Python 类型做转换和校验。
    # 它和普通 Pydantic BaseModel 目标不同：BaseModel 主要校验请求/响应结构，
    # BaseSettings 负责应用配置。FastAPI 当前也推荐用 pydantic-settings 管理这类配置。
    #
    # SettingsConfigDict：pydantic-settings 的配置字典。
    # env_file 指定 .env 来源；这里用绝对路径，避免必须在某个目录下启动应用。
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = ""
    db_name: str = "python_learn_v27"
    db_charset: str = "utf8mb4"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30
    db_pool_recycle: int = 1800

    @property
    def database_url(self) -> URL:
        # URL.create()：安全拼装数据库连接 URL，密码里的 @ : / 等字符不必手写百分号编码。
        # mysql+pymysql：mysql 是 SQLAlchemy dialect；pymysql 是 Python DBAPI driver。
        # SQLAlchemy 本身并不是 MySQL driver，真正对话 MySQL 的是 PyMySQL。
        return URL.create(
            drivername="mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={"charset": self.db_charset},
        )


settings = Settings()
