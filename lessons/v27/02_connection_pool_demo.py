"""
文件作用：观察 SQLAlchemy Engine 真实 Connection Pool 的 checkout / return。
实际意义：真实项目里 HTTP 请求不会每次新建 TCP 连 MySQL；需要看清连接从池里取出再还回去时状态如何变化。
运行命令：uv run python lessons/v27/02_connection_pool_demo.py
观察重点：A/B checkout 时的 CONNECTION_ID() 和 pool status；归还后再取 C，只观察是否可能复用，不断言 C 一定等于 A。
"""

from sqlalchemy import text

from app.database import describe_connect_error, engine


def demo_connection_pool() -> None:
    try:
        # engine.pool.status()：教学/调试时观察连接池状态的辅助信息，
        # 不是核心业务 API，也不应当成稳定监控协议。
        print("pool before =", engine.pool.status())

        conn_a = engine.connect()
        id_a = conn_a.execute(text("SELECT CONNECTION_ID()")).scalar()
        print(f"connection_id A={id_a}")
        print("pool after A checkout =", engine.pool.status())

        conn_b = engine.connect()
        id_b = conn_b.execute(text("SELECT CONNECTION_ID()")).scalar()
        print(f"connection_id B={id_b}")
        print("pool after A+B checkout =", engine.pool.status())

        conn_a.close()
        conn_b.close()
        print("pool after A+B return =", engine.pool.status())

        conn_c = engine.connect()
        id_c = conn_c.execute(text("SELECT CONNECTION_ID()")).scalar()
        print(f"connection_id C={id_c}")
        print("pool after C checkout =", engine.pool.status())
        conn_c.close()
        print("pool after C return =", engine.pool.status())
    except Exception as extra:
        print(describe_connect_error(extra))
        raise SystemExit(1) from extra


def main() -> None:
    demo_connection_pool()


if __name__ == "__main__":
    main()
