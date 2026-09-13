"""V15 复习笔记：V1～V14 核心映射（不是教程重写）。

运行：uv run python lessons/v15/review_notes.py
"""

NOTES = """
V1-V2  容器 / 推导式
  list/dict/set；[x for x in xs if ...] 过滤转换。
  数据已在内存时用普通 for / 推导式，不必假装异步。

V3     函数参数
  *args 收多余位置参数（tuple）；**kwargs 收多余关键字参数（dict）。
  默认参数不要用可变对象 [] / {}。

V4     模块
  用 python -m package.module 按包运行；import 时不要有业务副作用。

V5     异常
  业务失败用自定义 class（BizException 子类），不要全挤进 ValueError。
  except 具体类型；不要 except: pass。

V6     with
  with 管资源进入/释放。同步协议：__enter__ / __exit__。

V7-V8  class / dataclass
  dataclass 仍是 class，不是 TS interface。
  list 字段用 field(default_factory=list)。

V9     Iterator / Generator
  for -> __iter__ / __next__ / StopIteration。
  def + yield = Generator，惰性产出；yield 暂停，return 结束。

V10    typing
  标注给人和检查器看，默认不是运行时校验。
  type OrderId = int；Literal；X | None 表示值可能是 None，不等于参数可省略。

V11    decorator
  本质是函数包装。@wraps 保留元信息。
  带参 decorator 三层：配置 -> 接收 func -> wrapper。

V12    asyncio
  async def + return -> Coroutine。要 await 或变成 Task 才会推进。
  async 不等于自动并发；独立 IO 才用 gather。

V13    并发工具
  Semaphore = 限制同时进入的数量（进程内）。
  Lock = 保护共享状态临界区。
  Queue = 生产者消费者。都不是可靠任务队列。

V14    异步协议
  async with -> __aenter__ / __aexit__。
  async for -> __aiter__ / __anext__ / StopAsyncIteration。
  async def + yield -> Async Generator Object，用 async for / anext 消费。
  async with 不会把同步 open() 变成异步文件 IO。

V15 执行链
  main -> Service -> Repository -> 模拟 IO -> Model
  None -> raise BizException -> main 捕获
  独立 IO -> gather；批量 -> Semaphore；流 -> Async Generator；资源 -> async with
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v15 review_notes 运行完毕 ---")
