"""
文件作用：学习阶段用 create_all 在 MySQL 中创建 users 表。
实际意义：空库需要先有表，FastAPI User CRUD 才能写入真实 MySQL；这不是正式 Migration。
运行命令：uv run python lessons/v27/init_db.py
观察重点：打印当前库名和已存在的表；create_all 只是学习初始化，正式 schema 变更应使用 Alembic。
"""

from sqlalchemy import text

from app.database import describe_connect_error, engine, init_schema, list_tables


def main() -> None:
    try:
        init_schema()
        with engine.connect() as connection:
            database = connection.execute(text("SELECT DATABASE()")).scalar()
        print(f"database={database}")
        print(f"tables={list_tables()}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra


if __name__ == "__main__":
    main()
