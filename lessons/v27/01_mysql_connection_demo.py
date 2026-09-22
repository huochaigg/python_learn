"""
文件作用：真实连接 MySQL，读取 VERSION() 和当前 database。
实际意义：确认 SQLAlchemy / PyMySQL / 环境变量 / MySQL Server 四者真的连通，验证配置、driver、网络、账号权限、数据库名是否正确；不是为了重复学习 select。
运行命令：uv run python lessons/v27/01_mysql_connection_demo.py
观察重点：成功时打印真实 MySQL 版本和当前库名；失败时打印错误类别并退出，不会退回 SQLite。
"""

from sqlalchemy import text

from app.database import describe_connect_error, engine


def demo_mysql_connection() -> None:
    try:
        # engine.connect()：从 Engine 管理的连接池 checkout 一条 Connection；with 结束时归还。
        with engine.connect() as connection:
            version = connection.execute(text("SELECT VERSION()")).scalar()
            database = connection.execute(text("SELECT DATABASE()")).scalar()
            print(f"MySQL version={version}")
            print(f"database={database}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra


def main() -> None:
    demo_mysql_connection()


if __name__ == "__main__":
    main()
