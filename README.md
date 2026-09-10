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
