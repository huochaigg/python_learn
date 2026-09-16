"""V18 速查：Depends。

运行：uv run python lessons/v18/notes.py
"""

NOTES = """
Dependency callable
  普通函数 / class / generator 都行。FastAPI 在处理这一次 HTTP Request 时才调用。
  不是启动时执行一次，不是全局 singleton。

Depends
  Depends(get_pagination) 传函数引用。
  错误：Depends(get_pagination()) 会立刻调用，把返回值塞进去。

Annotated
  Annotated[PaginationParams, Depends(get_pagination)]
  类型给 IDE；Depends 给 FastAPI。老写法 = Depends(...) 能看懂即可。

Sub-dependency
  get_current_user 里再 Depends(get_token)。框架递归解析树。
  例：token → current_user → require_admin → endpoint

Class Dependency
  class 可调用，FastAPI 用它 new 实例再注入。endpoint 读 self.xxx。

yield dependency
  yield 前初始化；yield 的值注入 endpoint；yield 后（finally）清理。
  适合 DB Session。endpoint 抛错也要 close。

request cache
  默认 use_cache=True：同一 Request 内同一个 dependency 复用第一次结果。
  不是 Redis，不是 Nest Singleton。use_cache=False 仅用于理解。

Router-level dependency
  APIRouter(..., dependencies=[Depends(verify_xxx)]) 或装饰器 dependencies=[...]
  必须执行检查，但不把返回值注入函数参数。有点像 Guard 的一部分用途。

FastAPI vs NestJS DI
  都是依赖注入思想。
  Nest：Module/Provider/IoC，constructor 注入长期 Service 更常见。
  FastAPI：callable + 函数参数 + 每次请求现算的 dependency graph。
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v18 notes 运行完毕 ---")
