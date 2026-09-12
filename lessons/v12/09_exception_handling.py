"""V12-09 异步异常：await 的 try/except，以及 gather 的传播。

学习目标：
1. 会用 try/except 包住 await。
2. 看到 gather 里一个任务失败时，默认会把异常抛出来。
3. 眼熟 return_exceptions=True，但知道不能为了「不报错」滥用。

运行：uv run python lessons/v12/09_exception_handling.py
"""

import asyncio


async def load_ok() -> str:
    await asyncio.sleep(0.05)
    return "ok"


async def load_fail() -> str:
    await asyncio.sleep(0.05)
    raise ValueError("db timeout")


async def main() -> None:
    print("1) 单个 await 用 try/except")
    try:
        await load_fail()
    except ValueError as e:
        print("  捕获 =", e)

    print("2) gather 默认：任一失败，gather 本身抛错")
    try:
        await asyncio.gather(load_ok(), load_fail())
    except ValueError as e:
        print("  gather 抛出 =", e)

    print("3) return_exceptions=True：异常变成结果列表里的一项")
    # 用途：不想让一个失败打断整组时，把异常对象一并返回。
    # 坑：调用方必须自己检查 isinstance(item, Exception)，不能当成功数据用。
    # 不要为了「看起来不报错」到处开这个开关。
    mixed = await asyncio.gather(load_ok(), load_fail(), return_exceptions=True)
    print("  mixed =", mixed)
    for item in mixed:
        if isinstance(item, Exception):
            print("  需要自己识别失败项 =", item)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n--- 09 异步异常 运行完毕 ---")

# 本文件重点：
# 1. await 失败就是普通异常，用 try/except 即可。
# 2. gather 默认会把任务异常往外抛。
# 3. return_exceptions=True 把异常当返回值，必须显式检查。
# 4. create_task 后不管异常，错误可能被丢掉或拖到很晚才爆。
