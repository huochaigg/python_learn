"""V12-07 asyncio.gather()：并发等待多个异步操作。

学习目标：
1. 会用 gather 拿到按输入顺序排列的结果。
2. 知道它很像 Promise.all 的使用场景。
3. 看一眼：可以直接 gather coroutine，也可以 gather Task。

运行：uv run python lessons/v12/07_gather.py
"""

import asyncio


async def query_http() -> str:
    await asyncio.sleep(0.25)
    return "http:200"


async def query_db() -> str:
    await asyncio.sleep(0.15)
    return "db:user"


async def query_redis() -> str:
    await asyncio.sleep(0.1)
    return "redis:ok"


async def main() -> None:
    # asyncio.gather(*aws)：
    # 用途：同时推进多个异步操作，全部完成后返回结果元组（按传入顺序）。
    # JS 对比：≈ Promise.all([...]) 的使用场景。
    # 不是多线程，也不是多核并行；适合 IO Bound 一起等。
    print("直接 gather coroutine")
    http_res, db_res, redis_res = await asyncio.gather(
        query_http(),
        query_db(),
        query_redis(),
    )
    print("按输入顺序 =", http_res, db_res, redis_res)

    print("\n先 create_task 再 gather Task")
    t_http = asyncio.create_task(query_http())
    t_db = asyncio.create_task(query_db())
    t_redis = asyncio.create_task(query_redis())
    packed = await asyncio.gather(t_http, t_db, t_redis)
    print("同样按输入顺序 =", packed)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 07 gather 运行完毕 ---")

# 本文件重点：
# 1. gather 等一组 IO 全部完成，结果顺序跟参数顺序走。
# 2. 简单场景直接 gather coroutine 即可。
# 3. 需要提前启动/保存引用/以后取消时，再 create_task。
# 4. gather ≠ 多线程，解决的是「同时等待」。
