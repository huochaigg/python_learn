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

