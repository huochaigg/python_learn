# v0
uv init

uv add requests

uv run python main.py

# v1
uv run python lessons/v1/01_variables.py

uv run python lessons/v1/02_types.py

uv run python lessons/v1/03_conditionals.py

uv run python lessons/v1/04_loops.py

uv run python lessons/v1/05_functions.py

uv run python lessons/v1/06_containers.py

uv run python lessons/v1/07_Comprehensive.py

# v2
uv run python lessons/v2/01_list_advanced.py

uv run python lessons/v2/02_dict_advanced.py

uv run python lessons/v2/03_set_advanced.py

uv run python lessons/v2/04_unpacking.py

uv run python lessons/v2/05_comprehensions.py

uv run python lessons/v2/06_builtin_functions.py

uv run python lessons/v2/07_comprehensive.py

# v3
uv run python lessons/v3/01_function_arguments.py

uv run python lessons/v3/02_default_arguments.py

uv run python lessons/v3/03_args_kwargs.py

uv run python lessons/v3/04_keyword_only.py

uv run python lessons/v3/05_lambda.py

uv run python lessons/v3/06_scope.py

uv run python lessons/v3/07_function_as_object.py

uv run python lessons/v3/08_comprehensive.py

## v3 注意事项

- 关键字参数：`create_user(name="Tom", age=31)`，参数名本身是调用协议的一部分。
- 默认参数不要直接使用 list / dict / set 等可变对象；正确做法是默认 `None`，函数内部再创建新对象。
- `*args` 收集为 tuple；`**kwargs` 收集为 dict。
- 函数定义时 `*args` / `**kwargs` 是收集，函数调用时 `*data` / `**data` 是展开。
- `lambda` 只适合简单表达式；复杂逻辑优先普通 `def`。
- 正式项目尽量避免依赖 `global` 可变状态。

# v4
uv run python lessons/v4/01_import_basics.py

uv run python lessons/v4/02_custom_module.py

uv run python lessons/v4/03_package_basics.py

uv run python lessons/v4/04_absolute_import.py

uv run python lessons/v4/05_relative_import.py

uv run python lessons/v4/06_name_main.py

uv run python lessons/v4/greeter.py

uv run python lessons/v4/import_greeter.py

uv run python lessons/v4/07_module_side_effect.py

uv run python lessons/v4/08_comprehensive.py

uv run --directory lessons/v4 python -m demo_package.services.user_service

## v4 注意事项

- 一个 `.py` 文件可以作为 module。
- 目录可以组织成 package。
- `__init__.py` 可用于明确 package，并像前端 `index.ts` 那样统一导出。
- 优先理解绝对导入：从 package 根写完整路径，正式项目通常更清晰。
- 相对导入中的 `.` / `..` 基于 package，不完全等于磁盘上的相对路径。
- package 内模块出现相对导入时，不要随便直接 `python xxx.py`；可以使用 `python -m package.module`。
- `import` 会执行模块顶层代码。
- 避免 `import` 时产生数据库写入、网络请求等副作用。
- `if __name__ == "__main__":` 用于区分「直接运行」和「被 import」。

# v5
uv run python lessons/v5/01_try_except.py

uv run python lessons/v5/02_specific_exceptions.py

uv run python lessons/v5/03_else_finally.py

uv run python lessons/v5/04_raise.py

uv run python lessons/v5/05_custom_exception.py

uv run python lessons/v5/06_reraise_and_chain.py

uv run python lessons/v5/07_backend_scenario.py

uv run python lessons/v5/08_comprehensive.py

## v5 注意事项

- 优先捕获具体异常，例如 `except ValueError`、`except KeyError`。
- `except Exception` 只适合最终兜底场景，不要当成第一选择。
- 不要 `except: pass`，它会把真实 bug 吞掉。
- `else` 只在 try 成功时运行；`finally` 通常无论成功失败都会执行。
- `raise` 类似 JS `throw`；发现业务不满足要求就主动中断当前流程。
- 重新抛当前异常优先直接 `raise`，不要习惯性写 `raise e`。
- 自定义业务异常能提高代码语义，避免所有失败都用 `ValueError`。
- `raise XxxError(...) from e` 可以保留异常因果链。

# v6
uv run python lessons/v6/01_open_read.py

uv run python lessons/v6/02_write_append.py

uv run python lessons/v6/03_with_context.py

uv run python lessons/v6/04_pathlib.py

uv run python lessons/v6/05_json.py

uv run python lessons/v6/06_custom_context_manager.py

uv run python lessons/v6/07_backend_scenario.py

uv run python lessons/v6/08_comprehensive.py

## v6 注意事项

- `open()` 模式：`"r"` 只读且文件必须存在；`"w"` 覆盖写入；`"a"` 追加。
- Windows 文本文件建议显式 `encoding="utf-8"`。
- 手动 `open()` 不要忘记 `close()`；实际项目优先使用 `with`。
- `with` 会自动释放资源；Context Manager 的核心是 `__enter__` / `__exit__`。
- 大文件不要轻易 `read()` 全部载入内存，优先逐行读取。
- 路径处理优先考虑 `pathlib.Path`，并用 `Path(__file__)` 定位，不要写死绝对路径。
- `json.dumps` / `json.loads` 面向字符串，`json.dump` / `json.load` 面向文件。
- `ensure_ascii=False` 可保留中文；非法 JSON 读取会抛 `json.JSONDecodeError`。

# v7
uv run python lessons/v7/01_class_instance.py

uv run python lessons/v7/02_init_self.py

uv run python lessons/v7/03_instance_class_attributes.py

uv run python lessons/v7/04_instance_methods.py

uv run python lessons/v7/05_inheritance.py

uv run python lessons/v7/06_super_override.py

uv run python lessons/v7/07_dunder_isinstance.py

uv run python lessons/v7/08_backend_scenario.py

uv run python lessons/v7/09_comprehensive.py

## v7 注意事项

- Python 实例化不需要 `new`：写 `User()`，不是 `new User()`。
- `__init__` 类似 JS/TS `constructor`，负责给实例填初始数据。
- `self` 类似 JS `this`，但必须显式写在实例方法第一个参数；调用时不用手动传。
- `self.xxx` 通常是实例属性；写在 class 里、不在 `__init__` 里的是类属性。
- 类属性不要误用来保存每个实例独立的可变状态（共享 `list`/`dict` 会串数据）。
- `class Child(Parent)` 表示继承，对应 JS `class Child extends Parent`。
- `super()` 用于调用父类实现；子类自己写了 `__init__` 时记得 `super().__init__()`。
- `isinstance()` 支持继承判断，通常比 `type(x) == X` 更合适。
- `__str__()` 控制 `print(obj)` / `str(obj)` 时的可读字符串。

# v8
uv run python lessons/v8/01_instance_class_static.py

uv run python lessons/v8/02_classmethod_factory.py

uv run python lessons/v8/03_staticmethod.py

uv run python lessons/v8/04_property.py

uv run python lessons/v8/05_property_setter.py

uv run python lessons/v8/06_dataclass.py

uv run python lessons/v8/07_dataclass_field.py

uv run python lessons/v8/08_post_init.py

uv run python lessons/v8/09_backend_scenario.py

uv run python lessons/v8/10_comprehensive.py

## v8 注意事项

- 实例方法使用 `self`，操作「这个对象」。
- `@classmethod` 自动获得 `cls`（当前类），常用于 `create_xxx` / `from_xxx` 工厂方法；内部优先 `cls(...)`，不要写死类名。
- `@staticmethod` 不自动获得 `self` / `cls`，只是把和领域相关的普通函数放进类里。
- 需要当前实例状态 → 实例方法；需要类本身或工厂 → classmethod；都不依赖 → staticmethod。不属于该类的辅助逻辑也可以是模块级函数。
- `@property` 让方法看起来像属性：`user.full_name` 不加括号；getter 里不要藏耗时副作用。
- setter 内部通常用 `_age` 存值；`self.age = value` 会再次进入 setter，可能无限递归。
- `@dataclass` 自动生成 `__init__` / `__repr__` / `__eq__` 等样板；它是真正的 class，不是 TS interface。
- 可变默认字段使用 `field(default_factory=list)`，不要 `roles: list[str] = []`。
- `__post_init__` 在自动 `__init__` 之后做校验或补充逻辑。

# v9
uv run python lessons/v9/01_iterable.py

uv run python lessons/v9/02_iterator.py

uv run python lessons/v9/03_iter_next.py

uv run python lessons/v9/04_custom_iterator.py

uv run python lessons/v9/05_generator_basics.py

uv run python lessons/v9/06_yield_state.py

uv run python lessons/v9/07_generator_expression.py

uv run python lessons/v9/08_yield_from.py

uv run python lessons/v9/09_streaming_scenario.py

uv run python lessons/v9/10_comprehensive.py

## v9 注意事项

- Iterable 和 Iterator 不等价：list 等是 Iterable（数据来源），Iterator 才记录消费位置。
- `iter()` 从 Iterable 获取 Iterator；`next()` 获取下一项并推进状态。
- 耗尽后抛 `StopIteration`；`for` 会自动处理它。`next(it, default)` 可以改成返回默认值。
- Generator Function 调用返回 Generator Object；`yield` 会产出一个值并暂停，不是 `return` 那种结束。
- 一个 generator object 通常只能消费一次；要重新遍历需再次调用 generator function。
- `[]` 列表推导式立即得到完整 list；`()` Generator Expression 惰性计算。
- 大数据 / 流式场景可利用惰性计算减少一次性内存压力；不代表所有场景都该用 Generator。
- 后续 FastAPI `StreamingResponse` / SSE / Agent streaming 会继续使用「yield 一块、下游消费一块」这一思想。
- 本版不学 `send` / `throw` / 协程 / async generator，避免和同步 Generator 搅在一起。

# v10
uv run python lessons/v10/01_basic_typing.py

uv run python lessons/v10/02_union_optional.py

uv run python lessons/v10/03_literal.py

uv run python lessons/v10/04_type_alias.py

uv run python lessons/v10/05_typed_dict.py

uv run python lessons/v10/06_callable.py

uv run python lessons/v10/07_generic_function.py

uv run python lessons/v10/08_generic_class.py

uv run python lessons/v10/09_annotated_any_object.py

uv run python lessons/v10/10_backend_scenario.py

uv run python lessons/v10/11_comprehensive.py

## v10 注意事项

- Python 类型标注默认不等于运行时校验；解释器通常不会因为标错类型就立刻报错。以后 Pydantic/FastAPI 才会用 annotation 做运行时验证和框架元数据，本版不提前实现。
- 现代 Python 使用 `list[str]`、`dict[str, int]`，而不是必须 `List[str]`。
- Python 3.10+ 推荐使用 `A | B`；`Union` / `Optional` 是历史代码里常见的旧写法。
- `T | None` 表示允许 `None`；允许 None 不等于参数可以省略。调用时能否不传，通常还取决于有没有默认值，例如 `= None`。
- `Literal["admin", "user"]` 类似 TS 字面量联合类型，普通 Python 不会自动运行时拦错误字符串。
- 当前项目是 Python 3.12，类型别名优先 `type UserId = int`；`TypeAlias` 用来阅读旧项目。
- `TypedDict` 用于描述固定结构的 dict，不要和 dataclass / 普通 class / Pydantic BaseModel 混为一谈。
- `Callable[[int, int], int]` 描述函数签名：前面是参数类型，最后是返回值。
- `TypeVar` / `Generic` 用来保留「输入输出还是同一个 T」这种类型关系；不要用 `Any` 偷懒替代。
- Python 3.12 还支持 `def f[T]`、`class Box[T]` 新泛型语法，库代码里 `TypeVar`/`Generic` 仍然很常见。
- `Any` 应谨慎使用；`object` 更像「先收窄再当具体类型用」。
- `Annotated` 是「类型 + metadata」，后面 FastAPI 的 `Annotated[str, Query(...)]` 会重点重新学习，现在先眼熟。

# v11
uv run python lessons/v11/01_function_as_object_review.py

uv run python lessons/v11/02_closure.py

uv run python lessons/v11/03_basic_decorator.py

uv run python lessons/v11/04_decorator_syntax.py

uv run python lessons/v11/05_args_kwargs_return.py

uv run python lessons/v11/06_wraps.py

uv run python lessons/v11/07_decorator_with_args.py

uv run python lessons/v11/08_multiple_decorators.py

uv run python lessons/v11/09_backend_scenario.py

uv run python lessons/v11/10_comprehensive.py

## v11 注意事项

- Decorator 本质是接收函数并返回新函数；`@decorator` 大致等价于 `func = decorator(func)`。
- 装饰动作发生在函数定义/模块加载阶段；`wrapper` 里的逻辑发生在真正调用时，这两件事不是同一时刻。
- `wrapper` 常用 `*args/**kwargs` 兼容不同函数签名，内部再 `func(*args, **kwargs)`。
- 不要漏掉原函数返回值：应 `return func(...)` 或先接到 `result` 再 `return result`，否则外面拿到 `None`。
- 正式 decorator 通常使用 `functools.wraps` 保留 `__name__` / `__doc__`；不加的话名字往往会变成 `wrapper`。
- 带参数 decorator 会多一层配置函数：`@repeat(3)` 先执行 `repeat(3)` 得到真正的 decorator，再去接收下面的函数。
- 多个 decorator 按嵌套组合：`@A @B` 大致等于 `A(B(func))`。靠近函数的先包进去，调用时从外层走进去。
- 后端里 decorator 常用于日志、权限、缓存、重试、事务、耗时统计等横切逻辑。
- Decorator、Middleware、Interceptor 作用范围不同，不要简单认为是同一个东西。
- 本版只学同步函数 decorator，不涉及 async decorator。

# v12
uv run python lessons/v12/01_async_basics.py

uv run python lessons/v12/02_coroutine.py

uv run python lessons/v12/03_await_sleep.py

uv run python lessons/v12/04_event_loop.py

uv run python lessons/v12/05_sequential_vs_concurrent.py

uv run python lessons/v12/06_create_task.py

uv run python lessons/v12/07_gather.py

uv run python lessons/v12/08_blocking_problem.py

uv run python lessons/v12/09_exception_handling.py

uv run python lessons/v12/10_backend_scenario.py

uv run python lessons/v12/11_comprehensive.py

## v12 注意事项

- `async def` 调用返回 Coroutine Object，那不是最终结果。
- Coroutine 通常需要 `await`，或被包装成 Task 交给 Event Loop 调度，才会真正推进。
- `await` 会暂停当前 coroutine，把执行权交回 Event Loop，而不是把线程卡死。
- `asyncio.run(main())` 用于普通脚本启动/清理事件循环；FastAPI 已经自己管 loop，请求里不要再随便 `asyncio.run()`。
- `async` 不自动意味着并发。连续 `await a(); await b();` 仍然是串行。
- `asyncio.create_task()` 把 coroutine 调度成 Task；要保存引用并 `await`，不要创建完完全不管。
- `asyncio.gather()` 类似 `Promise.all` 的聚合场景：一起等完，结果按输入顺序返回。
- `time.sleep()` 会阻塞当前线程，在 Event Loop 线程里会拖死其他任务；`asyncio.sleep()` 暂停当前 coroutine 并让出执行权。
- asyncio 主要适合 HTTP / 数据库 / Redis / 网络等 IO Bound 工作，不是多核并行，也解决不了重 CPU Bound。
- 短生命周期 asyncio Task 与 BullMQ / Celery 这类可靠任务队列不是一回事。需要持久化、失败重试、跨进程、重启后继续，应使用任务队列，而不是单纯 `create_task`。

## v12 Node.js 对照

这些只是概念辅助映射，实现并不等同：

- `async def` ≈ `async function`
- `await` ≈ `await`
- `asyncio.gather()` ≈ `Promise.all`
- Python Coroutine 与 JS Promise 不完全等价：调用 Python async function 得到 coroutine，默认不会像 Promise 那样按同一套规则自动启动执行
- Task 可以理解为已经被 Event Loop 调度的 coroutine

# v13
uv run python lessons/v13/01_semaphore.py

uv run python lessons/v13/02_lock.py

uv run python lessons/v13/03_queue_basics.py

uv run python lessons/v13/04_producer_consumer.py

uv run python lessons/v13/05_timeout.py

uv run python lessons/v13/06_task_cancel.py

uv run python lessons/v13/07_taskgroup.py

uv run python lessons/v13/08_gather_vs_taskgroup.py

uv run python lessons/v13/09_backend_scenario.py

uv run python lessons/v13/10_comprehensive.py

## v13 注意事项

- 并发工具怎么选：`gather` = 聚合多个异步任务；`Semaphore` = 限制并发数量；`Lock` = 保护共享状态；`Queue` = 生产者消费者；`timeout` = 限制等待时间；`cancel` = 请求 Task 取消；`TaskGroup` = 结构化管理一组相关 Task。
- `Semaphore` 限当前进程内并发，不持久化任务；服务器重启、跨 Worker、重试仍要 Redis/BullMQ/Celery 等任务队列。
- `Lock` 保护的是 coroutine 临界区，不是 `threading.Lock`。
- 单线程 Event Loop 也不等于没有竞态：共享状态若是「读取 → await → 写入」，可能被其他 Task 插入。关键状态可用 Lock，但更优先减少共享可变状态。
- `Queue.get()` 只表示取到任务，不等于处理完成；处理完要 `task_done()`；`join()` 等待已入队任务都被标记完成。
- `asyncio.Queue` 是内存队列，进程重启后任务会丢失，不能替代可靠任务系统。
- `timeout` / `wait_for` 防止无限等待；超时抛 `TimeoutError`。
- `task.cancel()` 是协作式取消，不是强制杀进程；在 await 点以 `CancelledError` 形式送达。
- 捕获 `CancelledError` 做清理后通常继续 `raise`，不要随便吞掉。
- `TaskGroup` 用于结构化并发，减少孤儿 Task；`gather` 与 TaskGroup 不是简单替代关系。

# v14
uv run python lessons/v14/01_async_with_basics.py

uv run python lessons/v14/02_async_context_manager.py

uv run python lessons/v14/03_asynccontextmanager.py

uv run python lessons/v14/04_async_for_basics.py

uv run python lessons/v14/05_custom_async_iterator.py

uv run python lessons/v14/06_async_generator.py

uv run python lessons/v14/07_anext.py

uv run python lessons/v14/08_streaming_scenario.py

uv run python lessons/v14/09_backend_scenario.py

uv run python lessons/v14/10_comprehensive.py

## v14 注意事项

同步 / 异步协议对照：

- `with` ↔ `async with`
- `__enter__` / `__exit__` ↔ `__aenter__` / `__aexit__`
- `for` ↔ `async for`
- `__iter__` / `__next__` ↔ `__aiter__` / `__anext__`
- `StopIteration` ↔ `StopAsyncIteration`
- `def` + `yield` ↔ `async def` + `yield`

- `async with` 用于异步资源生命周期；核心协议是 `__aenter__` / `__aexit__`。
- `@asynccontextmanager` 可以通过 async generator 简化实现：yield 前进入，yield 出资源，yield 后清理。
- `async for` 消费 Async Iterable；每次下一项都可能需要等待。
- Async Iterator 使用 `__aiter__` / `__anext__`；结束时抛 `StopAsyncIteration`。
- `async def` + `yield` 是 Async Generator Function，调用得到 Async Generator Object。
- Async Generator 通常用 `async for` 或 `anext()` 消费，不能当成普通 coroutine 一次 `await` 完整个流。
- 普通同步资源不会因为写成 `async with` 就自动变成异步。`open()` 文件对象没有实现异步协议，也不会获得真正的异步文件 IO。
- 已经在内存里的 `list` 用普通 `for` 即可，不要为了「看起来异步」硬包成 Async Iterator。
- `async with` / `async for` 必须写在 `async def` 里。

## v14 后端联系

- 异步数据库 Session / Transaction 常使用 `async with`。
- 流式数据库 / API / AI 数据常使用 `async for`。
- SSE 和 Agent Streaming 可以使用 Async Generator 持续 `yield` 数据。
- 这些模式后续 FastAPI 阶段会重新结合真实框架学习。

# v15
uv run python -m lessons.v15.order_app.main

uv run python lessons/v15/review_notes.py

uv run python lessons/v15/checklist.py

## v15 项目结构

本版本开始从「单文件学习」切换到「多模块后端项目结构」。入口是 `lessons/v15/order_app/`：

- `models/`：数据模型（User / Order / OrderItem），用 dataclass + typing 描述业务对象。
- `repositories/`：数据访问。本课用 dict/list 模拟存储，并提供 FakeDatabaseSession。
- `services/`：业务规则（创建订单、库存、取消、并发详情、限流、状态流）。
- `exceptions/`：业务异常。Repository 可以返回 None，由 Service raise 明确错误。
- `utils/`：横切工具，例如日志 / 计时 / 权限 decorator。
- `main.py`：组装依赖并演示整条执行链，类似 NestJS 的 bootstrap。

对应 NestJS 的大致映射：DTO/Entity、Repository、Service、Exception、Utils、Bootstrap。

## v15 注意事项

- Repository 负责数据访问，Service 负责业务逻辑。
- Service 可以把 `None` 转换成明确业务异常，不要每一层都返回模糊的 None。
- constructor 注入依赖是依赖注入思想的基础；本课手动传入，不引入 DI 框架。
- 不要在 import 阶段执行真实业务副作用。
- `asyncio.gather` 用于独立 IO 聚合，不是多线程。
- `Semaphore` 只限制当前进程内并发，不是可靠任务队列。
- Async Context Manager（`__aenter__` / `__aexit__`）管理异步资源生命周期。
- Async Generator 可用于流式数据，调用端用 `async for` 消费。
- 内存 Repository 不是数据库；`async with` 也不会把同步对象自动变成异步。
- `inspect.iscoroutinefunction()` 用来判断函数是不是 coroutine function，从而决定 decorator 要不要 `await`。
- 本版本只是为 FastAPI 做过渡，不安装 FastAPI / SQLAlchemy / Redis。

## v15 阶段复习重点

- Python 类型标注不等于运行时校验。
- `str | None` 表示值可能是 None，不等于参数可以省略。
- dataclass 是 class，不是 TS interface；可变默认字段用 `field(default_factory=list)`。
- 异常是 class；业务失败用 `BizException` 子类，按类型捕获。
- decorator 本质是函数包装；带参 decorator 是三层结构；正式写法加 `wraps`。
- generator 惰性产出：`def` + `yield`。`async def` + `yield` 则是 Async Generator。
- `async` 不等于自动并发；Coroutine 与 Task 不同。
- `gather` 聚合一组独立 IO；`Semaphore` 限同时数量；`Lock` 保护共享状态。
- `async with` 对应 `__aenter__` / `__aexit__`；`async for` 对应 `__aiter__` / `__anext__`。
- 分层执行链：`main -> Service -> Repository -> 模拟 IO -> Model`。
- 出错链：`Repository 返回 None -> Service raise -> main 捕获并打印 Error Response`。

# v16
首次安装（已经装过就不用再跑）：

uv add "fastapi[standard]"

开发启动（当前官方 CLI）：

uv run fastapi dev lessons/v16/app/main.py

传统 Uvicorn 启动（理解 module:app 时用）：

uv run uvicorn lessons.v16.app.main:app --reload

`lessons.v16.app.main:app` 的意思：

- `lessons.v16.app.main`：Python 模块导入路径，对应文件 `lessons/v16/app/main.py`
- `app`：该模块里的变量 `app = FastAPI()`

访问入口（默认）：

- API：http://127.0.0.1:8000
- Swagger UI：http://127.0.0.1:8000/docs
- ReDoc：http://127.0.0.1:8000/redoc
- OpenAPI JSON：http://127.0.0.1:8000/openapi.json

学习文件：

uv run python lessons/v16/notes.py

uv run python lessons/v16/checklist.py

## v16 注意事项

- FastAPI 根据函数签名和 type annotation 推断参数来自 Path、Query 还是 Body。
- Path 参数名要和路由占位符一致，例如 `{user_id}` 对应 `user_id`。
- 简单且不在 Path 里的参数，通常作为 Query。
- 参数类型是 Pydantic `BaseModel` 时，通常作为 JSON Request Body。
- 普通 Python annotation 不等于运行时校验；但 FastAPI/Pydantic 会读取它并校验 HTTP 请求。
- `str | None` 只表示值可以是 None；真正「可以不传」通常还要 `= None`。
- Pydantic V2 优先 `model_dump()`；看到旧代码 `.dict()` 能认即可。
- `Query()` / `Path()` 给接口参数加约束；`Field()` 给 Body 模型字段加约束。
- 开发阶段优先 `uv run fastapi dev ...`；`uvicorn module:app` 用来理解底层启动方式。
- 路由可以用 `def` 或 `async def`。有 `await` 时再用 `async def`，不要机械全改 async。
- 本版本不拆 APIRouter，也不上 Depends / 数据库。

## v16 Swagger 测试清单

打开 http://127.0.0.1:8000/docs ，建议按这个顺序点：

正确请求：

- `GET /`、`GET /health`
- `GET /users/1`
- `GET /users?page=1&limit=20`
- `GET /users?keyword=Ada`
- `POST /users`，Body 例如 `{"name":"Tom","age":18,"email":"tom@example.com"}`
- `PUT /users/1?notify=true`，Body 只改部分字段
- `DELETE /users/{id}`（可以先 POST 一个再删）
- `GET /demo/plain-vs-fastapi`（看普通函数不会按 annotation 拦住错误类型）

故意错误（重点看 422，不要只测成功）：

- `GET /users/abc`：Path 无法转成 int
- `GET /users/0`：`Path(ge=1)` 失败
- `GET /users?limit=0` 或 `limit=999`：`Query(ge=1, le=100)` 失败
- `GET /users?keyword=` 超长字符串：`max_length` 失败
- `POST /users` 缺少 `name`
- `POST /users` 把 `age` 写成完全无法转换的值
- `POST /users` `name` 传空字符串：`Field(min_length=1)` 失败

观察响应里的 `detail` 校验数组即可，本课不自定义 validation error 格式。

## v16 NestJS 对照

- Nest `Controller` ≈ FastAPI 把 HTTP Method + Path 注册到处理函数；V16 先全部挂在一个 `app` 上，不是同一个模块系统。
- Nest `@Get` / `@Post` ≈ `@app.get` / `@app.post`：都是「把路由接到函数」，decorator 实现不同。
- Nest `@Param` / `@Query` / `@Body` ≈ FastAPI 多数时候靠函数签名推断；需要额外校验时再用 `Path()` / `Query()`。
- Nest DTO + class-validator ≈ Pydantic `BaseModel` + `Field` 的部分职责：解析、校验、序列化。
- Nest 常靠 `@ApiProperty` 等补 Swagger；FastAPI 大量文档可以直接从 typing / Pydantic 推导，仍然不是绝对等价。

# v17
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v17/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v17.app.main:app --reload --port 8001

`lessons.v17.app.main:app` 的意思：

- `lessons.v17.app.main`：Python 模块导入路径，对应文件 `lessons/v17/app/main.py`
- `app`：该模块里的变量 `app = FastAPI()`

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

学习文件：

uv run python lessons/v17/notes.py

uv run python lessons/v17/checklist.py

## v17 项目结构

- `main.py`：创建 `FastAPI()`，`include_router` 注册模块。应用组装，不堆 CRUD。
- `routers/users.py`：用户 Path Operation。`APIRouter(prefix="/users", tags=["users"])`。
- `routers/orders.py`：订单 Path Operation。独立 Router，证明接口不用堆回 main。
- `schemas/user.py`：`UserCreate` / `UserUpdate` / `UserPut` / `UserResponse`。HTTP 输入输出结构。
- `schemas/order.py`：`OrderCreate` / `OrderResponse`。和 users Schema 分开。

一句话：main 负责组装，Router 负责接口组织，Schema 负责 HTTP 输入输出结构。

## v17 注意事项

- `main.py` 不要继续堆所有接口。
- `APIRouter` 按业务拆分接口；`prefix` 自动拼接 URL；`tags` 主要用于 Swagger 分组。
- `include_router` 在启动阶段把 Router 注册到 App，不是发请求。
- Request Schema 和 Response Schema 要分离；不要对外返回 password。
- `response_model` 参与输出验证、序列化和字段过滤，不只是文档。
- 过滤能减少多余字段漏出，但不是唯一安全措施；本课不 Hash 密码。
- PATCH 常配合 `model_dump(exclude_unset=True)`，避免没提交的字段被默认 `None` 覆盖。
- PUT 偏向完整替换，PATCH 偏向部分修改；公司约定可能不同。
- `status.HTTP_201_CREATED` 等是语义化常量；204 不要带 JSON Body。
- 当前内存 dict 重启会丢失，不是真实数据层。

## v17 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，确认 users / orders 已经分组，然后：

- `POST /users`，Body 带 `name` / `email` / `password`；状态码应是 **201**
- 响应 JSON **没有 password**，尽管服务端内存里故意存了
- `GET /users`：数组里每一项也没有 password；文档应是 UserResponse 列表
- `GET /users/1`：单个 UserResponse
- `PATCH /users/1`，Body **只提交** `{"name":"Ada2"}`；再 GET，**email 仍是原来的值**，不是 null
- `PUT /users/1`，同时提交 `name` 和 `email`，观察完整替换公开字段
- `DELETE /users/{id}`：应是 **204** 且没有 JSON Body（可先 POST 一个再删）
- `POST /orders`、`GET /orders`：走另一套 Router / Schema
- 可选：`GET /users/demo/bad-response`，观察服务端 Response Validation Error（后端违约，不是客户端填错）

## v17 NestJS 对照

- Nest `Controller` 与 FastAPI `APIRouter`：都在按业务组织一组 HTTP 接口，不是同一个运行时。
- `@Controller("users")` 与 `APIRouter(prefix="/users")`：都给这组路由加前缀，拼 URL 的方式不同。
- Module 里登记 Controller，与 `app.include_router(...)`：都是应用组装，底层完全不是一回事。
- Request DTO / Response DTO 分开，与 Pydantic Request/Response Schema 分开：职责对应，校验库不同。
- 明确不是底层实现完全等价。

# v18
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v18/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v18.app.main:app --reload --port 8001

`lessons.v18.app.main:app`：前半是模块路径，最后一个 `app` 是 `main.py` 里的 FastAPI 实例。

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

学习文件：

uv run python lessons/v18/notes.py

uv run python lessons/v18/checklist.py

## v18 项目结构

- `main.py`：创建 App，注册 users / orders / demo Router。
- `dependencies/common.py`：可复用分页、Class Dependency、request marker。
- `dependencies/auth.py`：模拟 token → user → admin；以及只检查 Header 的 dependency。
- `dependencies/resources.py`：yield 假 Session / async client。
- `routers/users.py`、`routers/orders.py`：业务接口里复用分页；admin-only 看依赖链。
- `routers/demo.py`：cache / class / yield / header-check 等教学接口。
- `schemas/`：PaginationParams、CurrentUser 等演示用结构。

dependency 层放「可复用的请求解析、资源获取、鉴权检查」，不要变成随便塞业务逻辑的垃圾目录。本课 Header/token 只为理解 chain，真实 Auth 后续再做。

## v18 注意事项

- `Depends` 接收 callable，不要写成 `Depends(get_xxx())`。
- 推荐 `Annotated[T, Depends(get_xxx)]`；老项目 `param: T = Depends(get_xxx)` 能看懂即可。
- Dependency 可以继续 `Depends`；FastAPI 按树在**本次请求**里解析，不是启动时执行一次。
- class 也可以是 dependency：class 可调用，框架 new 出实例再注入。
- yield dependency 适合资源创建/清理；用 try/finally，不要假设 endpoint 一定正常 return。
- 默认 `use_cache=True` 是**同一 Request** 内复用，不是 Redis，不是 Nest 全局 Singleton。
- Router/path `dependencies=[Depends(...)]`：必须执行检查，但不注入返回值。
- 缺 Header / 校验失败走的是请求参数校验或 `HTTPException`，不是本课的全局 exception_handler。

## v18 执行链

鉴权链：

Request → get_token → get_current_user → require_admin → endpoint

资源链：

Request → create session → yield session → endpoint → finally cleanup session

分页链：

Request Query(page/limit/keyword) → get_pagination → PaginationParams → users/orders endpoint

## v18 NestJS 对照

- 两边都属于依赖注入思想：调用方不自己 `new` 全部协作对象。
- Nest 更偏 class / Provider / IoC Container，constructor injection 的 Service 往往跨请求活着。
- FastAPI 更偏 callable + 函数参数 + 每次请求现算的 dependency graph。
- Nest Guard 的部分「先检查再进 Controller」用途，可以用 FastAPI `dependencies=[...]` 或鉴权 dependency 近似，不是同一套机制。

## v18 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，同时看运行 FastAPI 的终端 print：

- `GET /users`、`GET /orders`：文档里应自动出现 page/limit/keyword；试 `limit=0` 应校验失败
- `GET /users/admin-only` 不带 `X-Token`：Header 校验失败
- 带 `X-Token: user-token` 访问 admin-only：应被拒绝
- 带 `X-Token: admin-token`：成功；终端顺序约是 get_token → get_current_user → require_admin → endpoint
- `GET /demo/query`：Class Dependency，看 skip/limit
- `GET /demo/session`：终端 session open → close
- `GET /demo/session-error`：接口会炸，终端仍应有 session close
- `GET /demo/async-client`：async open/close
- `GET /demo/cache-on`：marker 相同，get_request_marker 只 print 一次
- `GET /demo/cache-off`：两次执行，marker 不同
- `GET /demo/need-client`、`GET /demo/header-check`：需要 `X-Client: v18-demo`

# v19
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v19/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v19.app.main:app --reload --port 8001

`lessons.v19.app.main:app`：前半是模块路径，最后一个 `app` 是 `main.py` 里的 FastAPI 实例。

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

学习文件：

uv run python lessons/v19/notes.py

uv run python lessons/v19/checklist.py

## v19 项目结构

- `exceptions/`：`BizException` 及子类。只承载业务错误语义，不是 Response。
- `services/`：内存业务。查不到 / 库存不足时 raise 业务异常，不 raise HTTPException。
- `handlers/`：把异常转成 HTTP JSON。main 里 `register_exception_handlers(app)`。
- `routers/`：薄接口，调用 Service 后直接返回；不要到处 try/except BizException。
- `schemas/`：请求/响应结构；错误 body 保持简单 dict 即可。
- `main.py`：注册 handler + router。

一句话：Service 抛业务异常；Handler 转 HTTP；Router 保持薄；main 负责组装。

## v19 注意事项

- `HTTPException` 适合 HTTP 层错误（路由里明确的 401/404 Demo）。
- 复杂业务更适合自定义 `BizException`；Service 不要到处直接 raise HTTPException。
- 不要 Router 到处 `try/except`；让全局 handler 发挥作用。
- `exception_handler` 统一映射错误；不要把 Exception 对象或 traceback 返回客户端。
- `RequestValidationError` 与业务异常不同：前者是请求形状不对，后者是业务不允许。
- validation 默认/本课保持 **422**；统一错误结构不代表所有错误都返回 HTTP 200。
- 全局 Exception handler 只兜未知异常：HTTP 500 + 通用文案；详细 traceback 留在服务端日志。
- `raise ... from e` 保留因果链给调试；客户端仍只看到业务 JSON。
- 不要 `except Exception: return None`。未知异常不该被静默吞掉。
- `return {"error": ...}` 通常还是 200；失败请 `raise`。

## v19 错误执行链

请求参数错误：

Request → FastAPI/Pydantic 校验失败 → RequestValidationError → Validation Handler → **422**

业务不存在：

Request → Service raise UserNotFoundError → BizException Handler → **404** + `{code, message, data}`

库存不足（更具体 handler）：

Request → Service raise InsufficientStockError → Stock Handler → **409**（带 hint）

未知错误：

Request → RuntimeError → Global Exception Handler → **500**（客户端无 traceback）

## v19 NestJS 对照

- `throw new HttpException` ≈ FastAPI `raise HTTPException`（HTTP 层）。
- 自定义 `BizException` 思路相似：业务语义与 HTTP 映射分开。
- Nest `ExceptionFilter` ≈ FastAPI `exception_handler` / `add_exception_handler`。
- `ValidationPipe` 的请求校验职责，与 FastAPI/Pydantic 在进 endpoint 前的 validation 有部分对应。
- 机制和默认 JSON 形状并不完全一样。

## v19 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ：

- `GET /users/1`：正常用户
- `GET /users/99`：**404**，`code=USER_NOT_FOUND`，统一 body，没有 traceback
- `GET /orders/99`：**404** `ORDER_NOT_FOUND`
- `POST /orders` `{"user_id":1,"sku":"sku-2","qty":99}`：**409** 库存不足（可能多 `hint`）
- `POST /orders` `status` 填 `paid`：**400** `INVALID_ORDER_STATUS`
- `GET /demo/validation/abc` 或 `?limit=0`：**422** `VALIDATION_ERROR` + `errors`
- `GET /demo/unexpected-error`：**500** `INTERNAL_ERROR`；看终端日志有 traceback，响应没有
- `GET /demo/http-exception/0`：默认 HTTPException JSON（`detail`），和 BizException body 对照
- `GET /demo/http-exception-headers`：401，响应头带 `WWW-Authenticate` / `X-Demo-Reason`

# v20
首次安装（已经装过就不用再跑）：

uv add sqlalchemy

开发启动（端口统一 8001）：

uv run fastapi dev lessons/v20/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v20.app.main:app --reload --port 8001

纯 SQLAlchemy Demo（不经过 FastAPI，按模块跑才能 import lessons.v20）：

uv run python -m lessons.v20.sqlalchemy_demo

学习文件：

uv run python lessons/v20/notes.py

uv run python lessons/v20/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

SQLite 文件在 `lessons/v20/data/`（`app.db` 给 FastAPI，`demo.db` 给纯脚本），不要往项目根目录丢 `.db`。

## v20 项目结构

- `database.py`：Engine、`sessionmaker`、`get_db()` yield Session。
- `models/base.py`：`DeclarativeBase`。
- `models/user.py`：`Mapped` + `mapped_column` 的 User 表。
- `schemas/user.py`：Pydantic HTTP Schema（和 ORM 分开）。
- `services/user_service.py`：Session 上的 CRUD。
- `routers/users.py`：HTTP + `Depends(get_db)`。
- `sqlalchemy_demo.py`：先脱离 FastAPI 看 ORM 生命周期。

## v20 SQLAlchemy 核心关系

- **Engine**：管理数据库连接基础设施（URL、方言、连接池）。不是某一条 Connection。
- **sessionmaker / SessionLocal**：Session **工厂**。`SessionLocal()` 才创建 Session。
- **Session**：ORM 工作单元（查询、持久化、事务、对象状态）。需要时才从 Engine 取连接。Session ≠ Connection。
- **DeclarativeBase**：ORM Model 注册进同一套 mapping / metadata。
- **Mapped / mapped_column**：描述 ORM 属性与列配置。
- Session 绑定 Engine 后，CRUD 才会落到 SQLite 文件上。

## v20 CRUD 执行链

Create：`UserCreate` → `User()` → `session.add` → `commit`（必要时 `flush`/`refresh`）→ `UserResponse`

Query 列表：`select(User)` → `execute` → `scalars` → `all()` → ORM 列表

主键：`session.get(User, id)`

Update：`get` → 改 ORM 属性 → `commit`

Delete：`get` → `session.delete` → `commit`

请求链：FastAPI → `Depends(get_db)` → Session → Service → ORM → commit/query → ORM Object → Pydantic Response

## v20 注意事项

- 用 SQLAlchemy **2.x** 现代写法：`DeclarativeBase`、`Mapped`、`mapped_column`、`select()`。
- 不要优先学 `session.query(...)`（Legacy Query API）。
- Engine ≠ Connection；Session ≠ Connection。
- `SessionLocal` 是 factory，不是全局 Session；不要一个 Session 共享给所有请求。
- `add` ≠ `commit`；`flush` ≠ `commit`。
- `create_all` 不是 migration，不能当 Prisma migrate。
- Pydantic Schema 与 ORM Model 职责分离；Response 用 `from_attributes=True`。
- SQLite 仅用于当前学习；`check_same_thread=False` 是 SQLite 线程检查，不是万能连库参数。
- 本课不上 Alembic、Relationship、AsyncSession、MySQL。

## v20 Prisma 对照

- Prisma Model ≈ SQLAlchemy ORM Model（class ↔ 表，实例 ↔ 行）。
- Prisma Client 与 Session/Engine **只能辅助对照**：Client 更整包；SQLAlchemy 把 Engine 和 Session 拆开。
- `findUnique({ where: { id } })` 主键场景 ≈ `session.get(User, id)`。
- `findMany` ≈ `select(User)` + `execute` / `scalars`。
- `create` ≈ `User(...)` + `add` + `commit`。
- `update`：Prisma 偏 `update({ data })`；SQLAlchemy ORM 常改 Session 管理着的对象属性再 `commit`。

## v20 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ：

- `POST /users` 创建用户（带 email）
- 再用同一个 email POST 一次：观察 unique 冲突（本课映射成 409 `EMAIL_TAKEN`）
- `GET /users` 列表
- `GET /users/{id}` 主键查询
- `GET /users/99`：404 `USER_NOT_FOUND`
- `GET /users/by-email/{email}`：`select + where + scalar_one_or_none`
- `PATCH /users/{id}` 只改 `name`，其它字段保持
- `DELETE /users/{id}`：204；再 GET 同一 id 应为 404
- 停掉服务再启动：SQLite 文件还在，之前没删的用户仍能查到

# v21
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v21/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v21.app.main:app --reload --port 8001

先写入测试用户（已有数据会跳过，不会无限插入）：

uv run python -m lessons.v21.seed

查询表达式 Demo（独立 `demo.db`，会 print SQL）：

uv run python -m lessons.v21.query_demo

学习文件：

uv run python lessons/v21/notes.py

uv run python lessons/v21/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

SQLite 文件在 `lessons/v21/data/`（`app.db` 给 FastAPI，`demo.db` 给 query_demo），不要复用 V20 数据文件。

## v21 查询执行链

Query Params → 构建 `conditions=[]` → 动态 append SQL Expression → `select(User)` → `where(*conditions)` → `order_by` → `offset` / `limit` → `execute` → `scalars` → `items`

同一套 `conditions` → count query（不要带 offset/limit）→ `session.scalar` → `total` → `UserPageResponse`

## v21 注意事项

- SQLAlchemy Column / ORM Attribute 的 `==`、`>=` 生成 SQL Expression，不是立刻得到普通 Python bool。
- 动态条件用列表收集，不要为每个参数组合写大量 if/else 分支。
- bool Optional 判断使用 `is not None`；`if active:` 会把 `False` 误判成没有筛选。
- SQL OR 使用 `or_()`，不要用 Python `or` 连接两个 Expression。
- 排序字段必须做白名单映射（`"age": User.age`），禁止把前端字符串拼进 SQL。
- 分页必须明确稳定 `order_by`；没有 ORDER BY 时数据库不承诺返回顺序。
- COUNT 交给数据库（`func.count` + `scalar`），不要查出全部 ORM 再 `len()`。
- items 和 total 必须使用一致筛选条件，否则数量对不上。
- 不要通过 f-string 把用户输入拼进 SQL；参数走 bind parameters。

## v21 分页注意事项

- offset pagination 实现简单，适合普通后台 / 浅分页。
- 深分页时 OFFSET 越大可能越慢（数据库仍要跳过前面很多行）。
- 千万级订单等大数据场景，后续再学 cursor / keyset pagination。
- V21 暂时只把 offset pagination 学扎实。

## v21 Prisma 对照

- Prisma `where` 对象 ≈ SQLAlchemy `where` expression（SQLAlchemy 更强调表达式组合，并非 API 一一对应）。
- Prisma `orderBy` ≈ `order_by`。
- Prisma `skip` / `take` ≈ `offset` / `limit`。
- Prisma `count` ≈ `select(func.count(...))` + `session.scalar`。

## v21 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，先确认已运行 seed：

- `GET /users`：无条件列表（看 page / page_size / total / total_pages）
- `GET /users?keyword=Ada`：name 或 email 模糊匹配
- `GET /users?active=true`
- `GET /users?active=false`（确认停用用户能查到，没有被 `if active:` 丢掉）
- `GET /users?min_age=20&max_age=30`：年龄区间
- 多个条件组合：`keyword` + `active` + 年龄区间
- 不同排序字段：`sort_by=age` / `name` / `id` / `created_at`
- `sort_order=asc` 与 `sort_order=desc`
- `page` / `page_size` 翻页；超过范围的 page 应得到空 `items`，但 `total` 仍对
- 确认 `total` 与当前筛选条件下的 `items` 一致
- `GET /users/email-exists?email=user00@example.com`：EXISTS 只返回是否存在
- `GET /users/1`：主键拿对象

# v22
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v22/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v22.app.main:app --reload --port 8001

先写入测试订单（已有数据会跳过，不会无限插入）：

uv run python -m lessons.v22.seed

关系对象 / Lazy Loading Demo：

uv run python -m lessons.v22.relationship_demo

N+1 与 selectinload：

uv run python -m lessons.v22.n_plus_one_demo

三种加载策略（每段独立 Session）：

uv run python -m lessons.v22.relationship_loading_demo

selectinload vs joinedload，以及 join vs joinedload：

uv run python -m lessons.v22.selectinload_vs_joinedload

学习文件：

uv run python lessons/v22/notes.py

uv run python lessons/v22/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

SQLite 文件在 `lessons/v22/data/`（`app.db` 给 FastAPI，`relationship_demo.db` 给纯脚本），不要复用 V21 数据文件。

## v22 核心关系

- **ForeignKey** 是数据库层约束/引用：`OrderItem.order_id` 指向 `orders.id`。
- **relationship** 是 ORM 层对象导航：`Order.items` / `OrderItem.order`。`orders` 表不会真正生成 `items` 列。
- **Order.items** 是一对多 collection（`list[OrderItem]`）。
- **OrderItem.order** 是多对一 scalar（单个 `Order`）。
- **back_populates** 显式连接双向 relationship。SQLAlchemy 2.x 官方推荐这种写法，不要把 legacy `backref` 当主写法。

## v22 N+1

查询父对象列表后，循环访问尚未加载的 lazy relationship，可能产生 **1+N** 条 SQL（1 条订单列表 + N 条 items）。

`selectinload(Order.items)` 通常再发一条 `WHERE order_id IN (...)`，把子集合批量加载回来，是一对多场景的常见解法。

10 个订单的理想观察：items 相关查询从大约 11 条降到大约 2 条。具体 SQL 数量会受代码路径、Identity Map、缓存状态影响，不要写成永远保证。

## v22 selectinload vs joinedload

- **selectinload**：通常两阶段（父表查询 + 子表 IN 查询），不造成父行 JOIN 膨胀。
- **joinedload**：一条 JOIN 把关系数据一起取回；一对多大集合时，父行会在 SQL Result 里重复，数据量可能膨胀。
- 需要 `Result.unique()` 对 ORM Entity 去重。这不是 SQL `DISTINCT`。
- 不要简单认为「一条 SQL 一定比两条 SQL 快」。按关系基数和查询场景选择。

## v22 join vs joinedload

- **join()**：构造查询条件 / 过滤 / 排序，例如 `select(Order).join(Order.items).where(OrderItem.sku == sku)`。
- **joinedload()**：relationship 的 eager loading，目的是把 `order.items` 填上。
- 二者最终 SQL 都可能出现 JOIN，**意图不同**，不能因为名字都有 join 就混为一谈。

## v22 Response 注意事项

- `OrderResponse` 如果包含 `items`，查询时就应该明确加载关系（本课用 `selectinload`）。
- 不要等 Pydantic 序列化访问 `order.items` 时才意外触发大量 lazy SQL。
- 以后 `AsyncSession` 下，隐式 lazy IO 会更需要谨慎：asyncio 场景对 lazy loading 有额外限制。

## v22 Prisma 对照

- Prisma relation field 与 SQLAlchemy `relationship` 在目标上类似（对象图导航）。
- Prisma `include: { items: true }` 可以帮助理解 eager loading，但机制/API 不同。
- SQLAlchemy 需要你更明确地选择 lazy / selectinload / joinedload。

## v22 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，先确认已运行 seed：

- `POST /orders` 创建一笔带明细的订单（或依赖 seed 的 `ORD-000`～`ORD-009`）
- `GET /orders/{id}`：详情包含嵌套 `items`
- `GET /orders`：列表只有订单摘要，没有 `items`
- `GET /orders/with-items`：列表带关系数据
- `GET /orders/by-sku?sku=SKU-APPLE`：按 sku 过滤；`ORD-000` 有两条 Apple，结果里订单不应重复
- `GET /orders/9999`：不存在订单，404 `ORDER_NOT_FOUND`
- 在 Swagger Schemas 里对照嵌套的 `OrderResponse` / `OrderItemResponse`

# v23
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v23/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v23.app.main:app --reload --port 8001

初始化库存（已有数据会跳过；A001=10、B001=20、C001=5）：

uv run python -m lessons.v23.seed

查看库存：启动后 `GET /stocks`，或看 seed 打印。

手动 commit/rollback：

uv run python -m lessons.v23.transaction_demo

中间乱 commit 的错误示范：

uv run python -m lessons.v23.bad_transaction_demo

flush 不是 commit：

uv run python -m lessons.v23.flush_demo

`with session.begin()`：

uv run python -m lessons.v23.begin_demo

flush 失败后 rollback：

uv run python -m lessons.v23.rollback_after_flush_demo

下单原子性（失败对照成功，会打印事务前后库存/订单）：

uv run python -m lessons.v23.order_transaction_demo

学习文件：

uv run python lessons/v23/notes.py

uv run python lessons/v23/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs
- ReDoc：http://127.0.0.1:8001/redoc
- OpenAPI JSON：http://127.0.0.1:8001/openapi.json

SQLite 文件在 `lessons/v23/data/app.db`，不要复用 V22 数据文件。

## v23 事务核心

- 事务把多个数据库修改作为一个工作单元。
- 成功 `commit`；失败 `rollback`。
- **已经 commit 的事务不能被后续 rollback 撤销。**
- **flush 只是把 pending changes 同步到数据库，不代表最终提交。**
- 记住：`flush` = SQL 可能已经发出，但还没拍板；`commit` = 拍板；`rollback` = 把当前还没拍板的事务撤掉。

## v23 Order Transaction

`BEGIN` → 检查/扣库存过程中校验 → 创建 Order → `flush` 得到 `order.id` → 创建 OrderItems → 扣库存 → `COMMIT`

任意步骤异常 → `ROLLBACK` → 不留下半完成订单，库存也不部分扣减。

## v23 commit vs flush

- `add`：只是加入 Session 管理，不等于已经 INSERT 成功。
- `flush`：执行 pending SQL，但仍在事务内。
- `commit`：会先 flush，并最终提交。
- `rollback`：可以撤销尚未 commit 的修改。

## v23 常见错误

- 业务流程中间乱 `commit`（第一步留下，第二步失败撤不掉）。
- 把 `flush` 当成 `commit`。
- `rollback` 后吞掉异常 / `return None`。
- 数据库错误后不 `rollback`，又继续使用失败 Session。
- 每个小函数/Repository 自行决定 `commit`，事务无法跨操作组合。
- 以为 `rollback` 可以撤销以前已经 `commit` 的事务。

## v23 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，先确认已运行 seed：

- `GET /stocks`：查看初始库存（A001=10、B001=20、C001=5，若已下过单则以当前值为准）
- `POST /orders` 创建成功订单，例如 A001×2 + C001×1
- `GET /stocks`：对应库存减少；`GET /orders`：订单存在
- `POST /orders` 创建库存不足订单，例如 A001×1 + B001×999
- 确认 HTTP 业务错误 `INSUFFICIENT_STOCK`（409）
- 再 `GET /stocks`：没有部分扣减
- 再 `GET /orders`：失败订单没有残留

# v24
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v24/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v24.app.main:app --reload --port 8001

初始化库存：

uv run python -m lessons.v24.seed

Lost Update：

uv run python -m lessons.v24.concurrency_problem_demo

悲观锁 API（看 SQL，不把 SQLite 当行锁证据）：

uv run python -m lessons.v24.pessimistic_lock_demo

乐观锁 version：

uv run python -m lessons.v24.optimistic_lock_demo

原子 UPDATE + 多 SKU 事务：

uv run python -m lessons.v24.atomic_update_demo

三种方案对照：

uv run python -m lessons.v24.strategy_comparison

学习文件：

uv run python lessons/v24/notes.py

uv run python lessons/v24/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs

SQLite 文件在 `lessons/v24/data/app.db`。SQLite 用来学 ORM 和事务结构，**不要把它的 locking 行为等同于生产 MySQL/PostgreSQL**。

## v24 为什么事务还不够

Transaction 保证**一个事务自己的**多步操作原子性（V23：下单+明细+扣库存一起成功或一起失败）。

多个事务并发读取/修改同一行库存时，仍然可能 Lost Update / 超卖。这需要并发控制，不是再 commit 一次就能解决。

## v24 悲观锁

`SELECT ... FOR UPDATE` 在支持的数据库上锁定选中记录，直到事务结束。

适合冲突较高、锁内还要做复杂业务判断的临界区。缺点是等待、降低并发，以后还会碰到死锁。

`with_for_update()` 生成这句 SQL。锁的是数据库行，不是 Python Lock。

SQLite 不作为真实行锁实验依据。本课只学 API 和流程，等 MySQL/PostgreSQL 再做真实等待实验。

事务必须短：不要持锁调用外部支付，也不要把 `sleep(10)` 当正常写法。

## v24 乐观锁

读 `version=N`；更新时要求数据库仍然 `version=N`；成功后版本增加。别人已改过则 stale conflict。

SQLAlchemy `version_id_col` 可以为 **ORM flush 的 UPDATE/DELETE** 提供这套检查。

限制：直接 bulk `update()` / `delete()` **不会**自动获得同一套 version 检查。

冲突时先 `rollback`，再变成 `ConcurrencyConflictError` 抛出去，不要吞异常。

## v24 原子库存扣减

核心不是 `SELECT → if → UPDATE`，而是：

`UPDATE stock SET quantity = quantity - need WHERE sku=? AND quantity >= need`

然后检查 `rowcount`：1=成功，0=没有满足条件的行（SKU 不存在和库存不足是不同业务语义，本课在 0 时再查一次加以区分）。

多 SKU 放在一个 Transaction 中，任意一个失败则全部 rollback（V24 原子 UPDATE + V23 事务）。

## v24 三种方案怎么选

- 复杂、高冲突、锁内判断多：可以考虑悲观锁。
- 低冲突、编辑类、允许重试/失败：可以考虑乐观锁。
- 简单库存/余额/计数器：优先看条件原子 UPDATE 是否足够。

不写绝对性能排名，也不写「谁永远最好」。

## v24 常见错误

- 先 SELECT 库存再普通 UPDATE，以为包在事务里就一定不会超卖。
- 长时间持有 FOR UPDATE 锁（外部 IO / sleep）。
- 把 SQLite Demo 当成生产行锁行为。
- 加了 version 字段，却没有把它放进 UPDATE 条件（或没用 `version_id_col`）。
- bulk UPDATE 误以为自动走 `version_id_col`。
- 原子 UPDATE 后忘记 Transaction，多 SKU 会部分扣减。
- 看到高并发就直接上 Redis 分布式锁。

## v24 Swagger 测试清单

打开 http://127.0.0.1:8001/docs ，先 seed：

- `GET /stocks` 查看库存
- `POST /stocks/{sku}/atomic-deduct` 成功扣减
- 再扣到不够：`INSUFFICIENT_STOCK`
- `POST /orders/atomic` 三 SKU 都够：订单成功，库存都减少
- `POST /orders/atomic` 中途 C001 不够：业务错误；再 GET stocks，前面 A/B 的扣减全部 rollback
- 乐观锁主要跑 `optimistic_lock_demo`
- `POST /stocks/{sku}/pessimistic-deduct` 只观察 API；FOR UPDATE 等后续 MySQL/PostgreSQL 再做真实并发等待

## v24 后续学习

本课不讲：Transaction Isolation、MVCC 细节、死锁检测/重试、SAVEPOINT、Redis/Lua/Redlock、消息队列、分布式事务。这些以后单独学。

# v25
开发启动（端口统一 8001）：

uv run fastapi dev lessons/v25/app/main.py --port 8001

传统 Uvicorn 启动：

uv run uvicorn lessons.v25.app.main:app --reload --port 8001

数据库四类约束：

uv run python -m lessons.v25.constraints_demo

IntegrityError 与 rollback：

uv run python -m lessons.v25.integrity_error_demo

先查挡不住并发：

uv run python -m lessons.v25.race_unique_demo

Idempotency-Key：

uv run python -m lessons.v25.idempotency_demo

三层校验对照：

uv run python -m lessons.v25.constraint_vs_validation_demo

概念定位：

uv run python lessons/v25/concept_index.py

学习文件：

uv run python lessons/v25/notes.py

uv run python lessons/v25/checklist.py

访问入口：

- API：http://127.0.0.1:8001
- Swagger UI：http://127.0.0.1:8001/docs

SQLite 文件在 `lessons/v25/data/app.db`。

## v25 Demo 文件说明

- `constraints_demo.py`：看数据库四类约束（UNIQUE / NOT NULL / CHECK / ForeignKey）。
- `integrity_error_demo.py`：看约束失败后的 Session / rollback；另有「忘记 rollback」错误函数。
- `race_unique_demo.py`：两个 Session 都先查 email 不存在，最终只有一个 INSERT 成功。
- `idempotency_demo.py`：看 Idempotency-Key 防重复副作用。
- `constraint_vs_validation_demo.py`：Pydantic / Service / 数据库约束三层对照。
- `concept_index.py`：概念落到哪个文件、哪个函数。

## v25 概念定位

- UNIQUE → `constraints_demo.py` / `demo_unique()`
- NOT NULL → `constraints_demo.py` / `demo_not_null()`
- CHECK → `constraints_demo.py` / `demo_check_constraint()`
- ForeignKey 完整性 → `constraints_demo.py` / `demo_foreign_key()`
- IntegrityError → `integrity_error_demo.py` / `demo_integrity_error_flow()`
- 幂等 Key → `idempotency_demo.py` / `create_order_idempotent()`
- 先查不是并发保证 → `race_unique_demo.py` / `main()`
- 三层校验 → `constraint_vs_validation_demo.py` / `demo_three_layers()`

## v25 三层校验

- **Pydantic / FastAPI validation**：请求结构（类型、必填、长度）。
- **Service validation**：业务规则（email 已存在则友好错误）。
- **Database Constraint**：最终数据完整性（UNIQUE / NOT NULL / CHECK / FK）。

应用层判断是提前发现，数据库约束是最终兜底。不要混成一层。

## v25 UNIQUE 与并发

先查 email / Idempotency-Key 是否存在，只能改善用户体验，**不能消除并发竞争**。

两个请求都可能同时查到「不存在」。最终必须依靠数据库 UNIQUE（或其他并发机制）兜底。

## v25 IntegrityError 执行链

`INSERT/UPDATE` → 数据库约束失败 → `IntegrityError` → `rollback` → 转业务异常（如 `DuplicateEmailError`）→ V19 Exception Handler → HTTP JSON。

不要把数据库内部错误字符串直接返回前端。

## v25 幂等执行链

Request + `Idempotency-Key` → 查询是否已处理 → 已处理则返回已有结果；未处理则创建 → UNIQUE 兜底并发 → 重复冲突时重新读取已有结果。

幂等不是禁止重复请求，而是同一个业务请求重复执行时不要产生重复副作用。服务端不要随机生成 key。

## v25 常见错误

- 只做 Service 查询，不建 UNIQUE。
- 捕获 IntegrityError 后不 rollback。
- 把数据库内部错误字符串直接返回前端。
- 把 Pydantic validation 当数据库约束。
- 每次重试都生成新的 Idempotency-Key。
- 认为 POST 天然幂等。

## v25 Swagger 测试清单

- `POST /users` 创建用户；再用同一 email POST：409 `DUPLICATE_EMAIL`
- `POST /orders` 必须带 Header `Idempotency-Key`；缺了看 422
- 同一 Key、同一 body 再 POST 一次：还是同一条订单；`GET /orders` 只有一条
- 换一个 Key 再 POST：可以创建第二单
- `GET /orders/by-key/{idempotency_key}` 按 key 找回

本课不讲：MySQL/PostgreSQL error code、Deferrable Constraint、复合 UNIQUE、Upsert / ON CONFLICT、分布式幂等、Redis 幂等锁。

# v26
本版重点是事务隔离 / MVCC / 死锁。保留最小 FastAPI + SQLAlchemy 环境，用来证明 SQLite 里真有表和数据；隔离现象本身用可执行概念模型演示。

先初始化数据库：

uv run python lessons/v26/seed.py

FastAPI：

uv run fastapi dev lessons/v26/app/main.py --port 8001

等价 Uvicorn：

uv run uvicorn lessons.v26.app.main:app --reload --port 8001

隔离级别总览：

uv run python lessons/v26/isolation_overview_demo.py

脏读时间线：

uv run python lessons/v26/dirty_read_demo.py

不可重复读：

uv run python lessons/v26/non_repeatable_read_demo.py

幻读：

uv run python lessons/v26/phantom_read_demo.py

MVCC 快照思想：

uv run python lessons/v26/mvcc_demo.py

SQLAlchemy isolation_level API：

uv run python lessons/v26/isolation_level_demo.py

死锁循环等待：

uv run python lessons/v26/deadlock_demo.py

V23/V24/V26 对照时间线：

uv run python lessons/v26/transaction_timeline_demo.py

概念定位：

uv run python lessons/v26/concept_index.py

学习文件：

uv run python lessons/v26/notes.py

uv run python lessons/v26/checklist.py

## v26 Demo 文件说明

- `seed.py`：创建 `lessons/v26/data/v26.db` 的 `accounts` 表，幂等插入 A=100、B=200、C=50，再用 `select(Account)` 打印实际行。
- `isolation_overview_demo.py`：用 `ISOLATION_MATRIX` 对照四级隔离是否允许 dirty / non-repeatable / phantom，并 assert 标准意图。
- `dirty_read_demo.py`：SharedStore 同时维护 `committed_value` / `uncommitted_value`；A 写未提交 50，B 读到 50，A rollback 后 committed 仍 100。
- `non_repeatable_read_demo.py`：RC 模型两次读 100→50；snapshot 模型两次都是 100。
- `phantom_read_demo.py`：对用户列表 `age>=18` 做 filter；RC 下 2→3，snapshot 仍 2。
- `mvcc_demo.py`：运行简化版本可见性模型，通过 `snapshot_id` 选择可见 `RowVersion`；A 看见 10，C 看见 9。
- `isolation_level_demo.py`：真实调用 SQLAlchemy `Connection.get_isolation_level()` 和 `execution_options(isolation_level=...)`；SQLite 不支持的级别走 except。
- `deadlock_demo.py`：用 `threading.Lock` + `acquire(timeout=...)` 模拟 circular wait；再按 lock_a→lock_b 对照 consistent lock order。
- `transaction_timeline_demo.py`：用 Ledger/committed/snapshot 状态对象分别跑 V23 rollback、V24 Lost Update、V26 可见性。
- `concept_index.py`：打印概念 → 文件 → 函数，并 `getattr` 校验函数真实存在。

## v26 数据库验证

- seed 命令：`uv run python lessons/v26/seed.py`
- 数据库文件位置：`lessons/v26/data/v26.db`（由 `Path(__file__)` 推导，不依赖 cwd）
- 如何确认表已创建：seed 会 `init_db()` → import `Account` 后再 `Base.metadata.create_all`；成功后打印 `tables = ['accounts']`
- 如何确认数据已插入：seed 用 SQLAlchemy `select(Account)` 打印 A/B/C 三行；重复运行不会再插入
- 如何通过 FastAPI 查到数据：启动后访问 `GET /health`、`GET /accounts` 或 `GET /demo/data`

## v26 概念定位

- Isolation Level → `isolation_overview_demo.py` → `demo_isolation_matrix()`
- Dirty Read → `dirty_read_demo.py` → `demo_dirty_read()`
- Non-repeatable Read → `non_repeatable_read_demo.py` → `demo_read_committed_non_repeatable_read()` / `demo_repeatable_snapshot()`
- Phantom Read → `phantom_read_demo.py` → `demo_phantom_read()`
- MVCC → `mvcc_demo.py` → `demo_mvcc_snapshot_visibility()`
- Deadlock → `deadlock_demo.py` → `demo_circular_wait()`
- consistent lock order → `deadlock_demo.py` → `demo_consistent_lock_order()`
- SQLAlchemy isolation_level API → `isolation_level_demo.py` → `demo_get_and_change_isolation_level()`
- V23 原子性 → `transaction_timeline_demo.py` → `demo_v23_atomicity()`
- V24 Lost Update → `transaction_timeline_demo.py` → `demo_v24_lost_update()`
- V26 可见性 → `transaction_timeline_demo.py` → `demo_v26_visibility()`

## v26 四种隔离级别

| 级别 | 脏读 | 不可重复读 | 幻读（标准意图） |
| --- | --- | --- | --- |
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 挡 | 可能 | 可能 |
| REPEATABLE READ | 挡 | 挡* | 可能* |
| SERIALIZABLE | 挡 | 挡 | 挡 |

具体行为依赖数据库实现，不要仅凭标准名称推断 MySQL / PostgreSQL / SQLite 的全部细节。

## v26 三种并发现象

- **Dirty Read** = 读未提交。
- **Non-repeatable Read** = 同一行重复读取，字段值变了。
- **Phantom Read** = 相同范围查询的结果集合变了（多出行/少了行）。

## v26 MVCC

MVCC 通过多版本/快照控制事务可见性，提高读写并发。

MVCC != `version_id_col`（那是应用/ORM 检测 stale update）。

MVCC 也不等于「完全没有锁」。

## v26 Deadlock

循环等待；数据库通常会中止其中一个 transaction。

事务应尽量短。统一资源访问顺序可以降低风险，但不能保证绝对不死锁。

死锁后通常 rollback，再按策略重试**完整** transaction，不要从失败事务中间某条 SQL 继续跑。

## v26 与 V23/V24 的关系

- V23 Transaction = 一组操作的原子性。
- V24 并发更新策略 = 多事务竞争同一数据时怎么改。
- V26 Isolation/MVCC = 多事务并发时彼此能看到什么。

## v26 SQLite 限制

SQLite 用于当前 SQLAlchemy / 事务结构学习。

它不能完整代表 MySQL/PostgreSQL 的隔离级别、MVCC、FOR UPDATE、死锁行为。

Dirty Read / Non-repeatable Read / Phantom / MVCC 中部分文件属于「可执行概念模型」；Deadlock 是 Python 锁结构模拟。真正的双连接并发实验留给后续 MySQL/PostgreSQL 版本。

本课不讲：InnoDB undo log、read view、PostgreSQL xmin/xmax、gap/next-key lock、Predicate Lock、SSI、死锁图算法、自动重试 backoff。

# v27
本版第一次从 SQLite 切换到真实 MySQL。重点是：

`.env → BaseSettings → Settings → URL.create → create_engine`

以及：

`FastAPI Request → get_db → Session → Engine → Connection Pool → MySQL Connection → MySQL Server`，结束后 `Session.close` → Connection 回到 Pool。

依赖：

```
uv add pymysql pydantic-settings
```

本仓库已执行 `uv add pymysql`。`pydantic-settings` 已随 FastAPI 存在，未重复安装。不要加入 asyncmy / aiomysql（留给 V28）。

先复制环境变量模板并填写自己的账号（不要把真实密码写进 README 或提交 Git）：

```
copy lessons\v27\.env.example lessons\v27\.env
```

初始化表：

uv run python lessons/v27/init_db.py

连接与连接池：

uv run python lessons/v27/01_mysql_connection_demo.py

uv run python lessons/v27/02_connection_pool_demo.py

uv run python lessons/v27/03_session_lifecycle_demo.py

uv run python lessons/v27/04_db_health_demo.py

概念定位 / 笔记：

uv run python lessons/v27/concept_index.py

uv run python lessons/v27/notes.py

uv run python lessons/v27/checklist.py

FastAPI：

uv run fastapi dev lessons/v27/app/main.py --port 8001

等价 Uvicorn：

uv run uvicorn lessons.v27.app.main:app --reload --port 8001

## v27 MySQL 前置准备

需要本机已有可访问的 MySQL 8.x（或兼容 MySQL Server）。本课不会自动安装或启动 Docker MySQL。

先创建数据库（不要 DROP 已有库）：

```sql
CREATE DATABASE python_learn_v27 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

如果 `.env` 配错或 MySQL 没开，程序会指出是 driver 未安装、host/port 不通、access denied 还是 database 不存在，不会退回 SQLite。

## v27 .env 配置

- `lessons/v27/.env.example` 可以提交，里面是占位符 `your_password`。
- 真实 `lessons/v27/.env` 由本地填写，已被 `.gitignore` 忽略，不要提交。
- 不要把真实密码写进 README、代码或 Git。
- 不要在日志或 `/health/db` 里返回完整 DATABASE_URL / username / password。

## v27 Demo 学习顺序

1. `01_mysql_connection_demo.py`：先确认四者连通。
2. `02_connection_pool_demo.py`：观察 checkout / return。
3. `03_session_lifecycle_demo.py`：观察 Session 生命周期。
4. `04_db_health_demo.py`：观察 SELECT 1 健康检查。
5. 启动 FastAPI app（先跑 `init_db.py` 建表）。
6. 打开 Swagger 测试真实 User CRUD：`POST /users`、`GET /users`、`GET /users/{id}`。

## v27 Demo 文件说明

- `01_mysql_connection_demo.py`：确认 SQLAlchemy / PyMySQL / `.env` / MySQL Server 真能连上，并读出版本和当前库名。
- `02_connection_pool_demo.py`：用真实 Engine Pool checkout 多条 Connection，打印 `CONNECTION_ID()` 和 `pool.status()`。
- `03_session_lifecycle_demo.py`：创建两个不同 Session，证明 Session 不是 Connection，close 只结束 Session。
- `04_db_health_demo.py`：调用与 `/health/db` 相同的 `check_db_health()`，真实执行 `SELECT 1`。
- `init_db.py`：学习用 `create_all` 建 `users` 表，不是 Alembic Migration。

## v27 概念定位

- 真实 MySQL 连接 → `01_mysql_connection_demo.py` → `demo_mysql_connection()`
- Connection Pool → `02_connection_pool_demo.py` → `demo_connection_pool()`
- pool_size/max_overflow → `app/database.py` → `create_engine`
- pool_pre_ping → `app/database.py`
- pool_recycle → `app/database.py`
- Session 生命周期 → `03_session_lifecycle_demo.py` → `demo_session_lifecycle()`
- DB Health → `04_db_health_demo.py` + `app/routers/health.py` → `demo_db_health()` / `check_db_health()`
- Settings/.env → `app/config.py` → `Settings`

## v27 Engine / Pool / Session 执行链

应用启动 → 创建 Engine → Engine 管理 Pool。

HTTP Request → `Depends(get_db)` → Session → 从 Engine/Pool 获取 Connection → SQL → `Session.close()` → Connection 回 Pool。

`Session.close()` 通常不等于永久关闭底层 MySQL TCP connection。

## v27 连接池参数

当前数字只是学习配置，不是生产推荐值。真实值要看数据库 `max_connections`、应用 worker 数量和负载测试。

- `pool_size`：池里长期维持的基础连接数。不是 FastAPI 能同时处理的 HTTP 上限。
- `max_overflow`：基础连接都被占用时，还能临时再开多少条。不是数据库最大连接数。
- `pool_timeout`：池里暂时没连接时，最多等多少秒。超时常见 QueuePool timeout。
- `pool_pre_ping`：checkout 时先确认连接还活着，处理 stale connection。不是每条 SQL 都 ping。
- `pool_recycle`：连接太老则下次取出时重建，应对 MySQL 长连接超时。不是每 N 秒重启整个池。

如果以后 FastAPI 启动多个 worker，每个进程通常各自拥有自己的 Engine/Pool。总数据库连接潜力会随 worker 数增加，不要以为 `pool_size=5` 就是整个系统永远只有 5 个连接。

## v27 安全注意事项

- 不要 hard-code DB password。
- 不要把完整 DATABASE_URL 打进日志。
- 不要提交 `.env`。
- 健康检查不要返回敏感连接配置。

# v28
本版是「真实 MySQL 同步 SQLAlchemy → Async SQLAlchemy」的升级。继续连同一台 MySQL Server，但使用独立库 `python_learn_v28`，避免覆盖 V27 数据。不 fallback 到 SQLite，也不改回 PyMySQL。

目标执行链：

`async def endpoint → Depends(get_db) → AsyncSession → await execute/commit → AsyncEngine → asyncmy → MySQL`

依赖：

```
uv add asyncmy
```

已执行 `uv add asyncmy`。`greenlet` 已随 SQLAlchemy 存在，未重复安装。V27 的 `pymysql` 保留。

先复制环境变量模板并填写自己的账号（不要把真实密码写进 README 或提交 Git）：

```
copy lessons\v28\.env.example lessons\v28\.env
```

初始化表：

uv run python lessons/v28/init_db.py

AsyncEngine 连接：

uv run python lessons/v28/01_async_connection_demo.py

uv run python lessons/v28/02_async_session_demo.py

uv run python lessons/v28/03_async_transaction_demo.py

uv run python lessons/v28/04_async_relationship_demo.py

概念定位 / 笔记：

uv run python lessons/v28/concept_index.py

uv run python lessons/v28/notes.py

uv run python lessons/v28/checklist.py

FastAPI：

uv run fastapi dev lessons/v28/app/main.py --port 8001

等价 Uvicorn：

uv run uvicorn lessons.v28.app.main:app --reload --port 8001

## v28 MySQL 前置准备

需要本机已有可访问的 MySQL 8.x。本课不会自动安装 Docker。先建独立库（不要 DROP 已有库）：

```sql
CREATE DATABASE python_learn_v28 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

`.env.example` 可以提交；真实 `.env` 不提交。健康检查不要返回 URL / password。

## v28 同步/异步 API 对照

| 同步 | 异步 |
| --- | --- |
| `create_engine` | `create_async_engine` |
| `sessionmaker` | `async_sessionmaker` |
| `Session` | `AsyncSession` |
| `with session` | `async with session` |
| `session.execute` | `await session.execute` |
| `session.commit` | `await session.commit` |
| `session.get` | `await session.get` |
| `session.flush` | `await session.flush` |
| `session.rollback` | `await session.rollback` |

`select()` / `where()` / `order_by()` 仍然只是构造 Statement，不 await。

## v28 Demo 学习顺序

1. `01_async_connection_demo.py`
2. `02_async_session_demo.py`
3. `03_async_transaction_demo.py`
4. `04_async_relationship_demo.py`
5. `init_db.py`
6. FastAPI app + Swagger

`02` 以后若提示表不存在，先跑 `init_db.py`。

## v28 Demo 文件说明

- `01_async_connection_demo.py`：确认 asyncmy + AsyncEngine + MySQL 真能连上，并用 await 读版本和当前库。
- `02_async_session_demo.py`：用 AsyncSession 查 users；两个独立 Session 再 `gather`，演示 Session per Task。
- `03_async_transaction_demo.py`：成功事务能看到新订单；失败事务 rollback 后数据不留下。
- `04_async_relationship_demo.py`：`selectinload(Order.items)` 后打印 order_no 和 sku 列表。
- `init_db.py`：`run_sync(Base.metadata.create_all)` 在 MySQL 建表，不是 Alembic。

## v28 概念定位

- AsyncEngine → `app/database.py` → `create_async_engine`
- asyncmy Driver → `app/config.py` → `database_url`
- async_sessionmaker → `app/database.py` → `async_sessionmaker`
- AsyncSession → `app/database.py` / `02_async_session_demo.py` → `demo_async_session`
- expire_on_commit=False → `app/database.py` → `AsyncSessionLocal`
- async get_db → `app/database.py` → `get_db`
- await execute → `app/services/*` + `02_async_session_demo.py` → `demo_async_session`
- async transaction → `03_async_transaction_demo.py` → `demo_async_transaction`
- run_sync(create_all) → `init_db.py` → `main`
- async relationship/selectinload → `04_async_relationship_demo.py` → `demo_async_relationship`
- AsyncSession per Task → `notes.py` + `02_async_session_demo.py` → `demo_async_session`

## v28 AsyncSession 生命周期

Request → `Depends(get_db)` → AsyncSession → AsyncEngine → Pool → asyncmy → MySQL。

Request 结束 → AsyncSession close → Connection 回 Pool。

## v28 await 判断原则

构造 SQL Expression 不 await；会真正产生数据库 IO 的 AsyncSession / AsyncConnection coroutine 需要 await。

- 不 await：`select()`、`where()`、`order_by()`、`options()`、`session.add()`
- 要 await：`execute()`、`commit()`、`flush()`、`refresh()`、`rollback()`、`get()`、`delete()`

## v28 并发注意事项

AsyncSession 是有状态 transaction object，不能在多个 asyncio Task 中并发共享。需要并发 DB Task 时通常 Session per task，但这会改变事务边界和连接占用，需要谨慎。

## v28 Relationship 注意事项

Async ORM 更要避免隐式 lazy IO。需要关系字段时优先 `selectinload` 等 eager loading。不要等 Pydantic Response 序列化时才触发数据库查询。

## v28 常见错误

- 只把 endpoint 改 async，但还用 PyMySQL 同步 Driver
- 每请求 `create_async_engine`
- 给 `select()` 加 await
- 忘记 await `execute` / `commit` / `rollback`
- 多个 gather Task 共用一个 AsyncSession
- 使用 relationship lazy loading 导致隐式 IO
- 每请求 `dispose` Engine

# v29
V28 之上接入 OpenAI Agents SDK。详细说明见 `lessons/v29/README.md`。

推荐先跑：

uv run python lessons/v29/01_agent_basic_demo.py

FastAPI：

uv run fastapi dev lessons/v29/app/main.py --port 8001

# v30
V29 之上做 SDK Streaming + FastAPI SSE。详细说明见 `lessons/v30/README.md`。

推荐先跑：

uv run python lessons/v30/01_basic_stream_demo.py

FastAPI：

uv run fastapi dev lessons/v30/app/main.py --port 8001

# v31
V30 之上做 SDK Session + MySQL 会话历史。详细说明见 `lessons/v31/README.md`。

推荐先跑：

uv run python lessons/v31/01_sqlite_session_demo.py

FastAPI：

uv run fastapi dev lessons/v31/app/main.py --port 8001

