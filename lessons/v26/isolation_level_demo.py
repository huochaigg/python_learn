"""
文件作用：真实调用 SQLAlchemy Connection 读取/切换 isolation_level；不支持的级别 try/except，不伪造结果。
运行命令：uv run python lessons/v26/isolation_level_demo.py
重点概念：get_isolation_level、execution_options(isolation_level=...)、SQLite 支持子集、AUTOCOMMIT。
观察重点：当前 SQLite 能读到实际级别；READ UNCOMMITTED 可切换；REPEATABLE READ 应明确报不支持。
"""

from pathlib import Path

from sqlalchemy import create_engine, text

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "v26.db"


def demo_get_and_change_isolation_level() -> str:
    # 复用 V26 主库路径，避免再生成一个空的 isolation_level_demo.db。
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.connect() as connection:
        # get_isolation_level()：读取当前 Connection 实际隔离级别，各库返回值不必相同。
        current = connection.get_isolation_level()
        print("db =", DB_PATH)
        print("current =", current)
        assert current in {"SERIALIZABLE", "READ UNCOMMITTED"}

    with engine.connect() as connection:
        # execution_options(isolation_level=...)：必须在新事务/autobegin 之前设置。
        # isolation_level 可用值由 dialect 决定。SQLite 常见 SERIALIZABLE / READ UNCOMMITTED。
        connection = connection.execution_options(isolation_level="READ UNCOMMITTED")
        changed = connection.get_isolation_level()
        print("after READ UNCOMMITTED =", changed)
        assert changed == "READ UNCOMMITTED"
        connection.execute(text("SELECT 1"))

    with engine.connect() as connection:
        try:
            connection.execution_options(isolation_level="REPEATABLE READ")
            print("REPEATABLE READ accepted =", connection.get_isolation_level())
            raise AssertionError("SQLite 不应接受 REPEATABLE READ")
        except AssertionError:
            raise
        except Exception as extra:
            print(
                "当前 SQLite dialect 不支持 REPEATABLE READ，后续 MySQL/PostgreSQL 再实测:",
                type(extra).__name__,
            )

    engine.dispose()
    # AUTOCOMMIT 是 DBAPI 事务行为模式，不是第五种标准隔离级别。本函数不作为主路径。
    print("实际结果总结：SQLite 可读到隔离级别；支持的值可切换；不支持的级别走 except，不伪造。")
    return current


def main() -> None:
    demo_get_and_change_isolation_level()


if __name__ == "__main__":
    main()
    print("--- v26 isolation_level_demo 运行完毕 ---")
