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
