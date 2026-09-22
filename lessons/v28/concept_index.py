"""
文件作用：V28 概念定位索引。只列出概念落在哪个文件/函数。
运行命令：uv run python lessons/v28/concept_index.py
观察重点：回头查概念时先看这里，再打开对应文件。
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_demo(filename: str, modname: str):
    spec = spec_from_file_location(modname, ROOT / filename)
    if spec is None or spec.loader is None:
        raise RuntimeError(filename)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


demo01 = load_demo("01_async_connection_demo.py", "async_connection_demo")
demo02 = load_demo("02_async_session_demo.py", "async_session_demo")
demo03 = load_demo("03_async_transaction_demo.py", "async_transaction_demo")
demo04 = load_demo("04_async_relationship_demo.py", "async_relationship_demo")

CONCEPT_INDEX = [
    ("AsyncEngine", "app/database.py", "create_async_engine", None),
    ("asyncmy Driver", "app/config.py", "database_url", None),
    ("async_sessionmaker", "app/database.py", "async_sessionmaker", None),
    ("AsyncSession", "app/database.py / 02_async_session_demo.py", "demo_async_session", demo02),
    ("expire_on_commit=False", "app/database.py", "AsyncSessionLocal", None),
    ("async get_db", "app/database.py", "get_db", None),
    ("await execute", "app/services/* + 02_async_session_demo.py", "demo_async_session", demo02),
    ("async transaction", "03_async_transaction_demo.py", "demo_async_transaction", demo03),
    ("run_sync(create_all)", "init_db.py", "main", None),
    ("async relationship/selectinload", "04_async_relationship_demo.py", "demo_async_relationship", demo04),
    ("AsyncSession per Task", "notes.py + 02_async_session_demo.py", "demo_async_session", demo02),
]


def main() -> None:
    print("===== V28 concept_index =====")
    for name, location, func_name, module in CONCEPT_INDEX:
        if module is not None:
            func = getattr(module, func_name, None)
            assert callable(func), f"{location} 缺少 {func_name}()"
        print(f"{name} → {location} → {func_name}")


if __name__ == "__main__":
    main()
