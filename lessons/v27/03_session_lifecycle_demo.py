"""
文件作用：创建两个不同 Session，分别查询，并观察 close 前后的公开状态。
实际意义：理解 Session != Connection。Session 生命周期按请求/工作单元结束；Engine/Pool 在应用进程里长期存在。
运行命令：uv run python lessons/v27/03_session_lifecycle_demo.py
观察重点：两个 Session 对象身份不同；查询后存在 transaction，close 后 get_transaction() 为 None。
"""

from sqlalchemy import text

from app.database import SessionLocal, describe_connect_error


def demo_session_lifecycle() -> None:
    try:
        session_a = SessionLocal()
        result_a = session_a.execute(text("SELECT 1")).scalar()
        print(
            f"session_a id={id(session_a)} has_transaction={session_a.get_transaction() is not None} "
            f"SELECT 1={result_a}"
        )
        session_a.close()
        print(f"session_a after close has_transaction={session_a.get_transaction() is not None}")

        session_b = SessionLocal()
        result_b = session_b.execute(text("SELECT DATABASE()")).scalar()
        print(
            f"session_b id={id(session_b)} has_transaction={session_b.get_transaction() is not None} "
            f"DATABASE()={result_b}"
        )
        session_b.close()
        print(f"session_b after close has_transaction={session_b.get_transaction() is not None}")
        print(f"same_object={session_a is session_b}")
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra


def main() -> None:
    demo_session_lifecycle()


if __name__ == "__main__":
    main()
