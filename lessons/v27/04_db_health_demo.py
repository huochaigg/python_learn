"""
文件作用：调用与 FastAPI /health/db 相同的 check_db_health()，真实执行 SELECT 1。
实际意义：验证「应用进程活着」和「应用能连接数据库」是两个不同健康状态；进程 up 不等于 MySQL 可达。
运行命令：uv run python lessons/v27/04_db_health_demo.py
观察重点：SELECT 1 的实际返回值、database=mysql、db_name；响应里不能出现密码或完整 DATABASE_URL。
"""

from app.database import SessionLocal, check_db_health, describe_connect_error


def demo_db_health() -> None:
    session = SessionLocal()
    try:
        result = check_db_health(session)
        print(f"status={result['status']}")
        print(f"database={result['database']}")
        print(f"db_name={result['db_name']}")
        print(f"SELECT 1={result['select_1']}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra
    finally:
        session.close()


def main() -> None:
    demo_db_health()


if __name__ == "__main__":
    main()
