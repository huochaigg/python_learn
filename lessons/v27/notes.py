"""
文件作用：V27 速查。Settings、Engine、Pool、Session、健康检查各记几行。
运行命令：uv run python lessons/v27/notes.py
观察重点：能画出 FastAPI Request → Session → Engine → Pool → MySQL 这条链。
"""

NOTES = """
.env → BaseSettings → Settings → URL.create → create_engine
  配置从环境变量来，不要把密码写进代码。

Engine
  单个应用进程里长期复用。不要每个请求 create_engine。

Connection Pool
  Engine 管理一组 MySQL 连接。checkout 使用，close/归还后通常回到池里。

pool_size
  池里长期维持的基础连接数。不是 FastAPI 并发上限。

max_overflow
  基础连接用完后还能临时再建多少条。不是数据库 max_connections。

pool_timeout
  池暂时没连接时最多等多久。超时是 QueuePool timeout。

pool_pre_ping
  checkout 时先确认连接还活着。不是每条 SQL 都 ping。

pool_recycle
  连接太老则下次取出时重建。应对 MySQL 长连接超时，不是定时重启整个池。

Session
  一次工作单元。Session.close() 结束 Session，底层连接通常回池，不等于拆掉 TCP。

/health vs /health/db
  进程活着 不等于 数据库连得上。
"""


def main() -> None:
    print(NOTES)


if __name__ == "__main__":
    main()
