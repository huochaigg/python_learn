"""
文件作用：V27 概念定位索引。只列出概念落在哪个文件/函数。
运行命令：uv run python lessons/v27/concept_index.py
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


demo01 = load_demo("01_mysql_connection_demo.py", "mysql_connection_demo")
demo02 = load_demo("02_connection_pool_demo.py", "connection_pool_demo")
demo03 = load_demo("03_session_lifecycle_demo.py", "session_lifecycle_demo")
demo04 = load_demo("04_db_health_demo.py", "db_health_demo")

CONCEPT_INDEX = [
    ("真实 MySQL 连接", "01_mysql_connection_demo.py", "demo_mysql_connection", demo01),
    ("Connection Pool", "02_connection_pool_demo.py", "demo_connection_pool", demo02),
    ("pool_size/max_overflow", "app/database.py", "create_engine", None),
    ("pool_pre_ping", "app/database.py", "create_engine", None),
    ("pool_recycle", "app/database.py", "create_engine", None),
    ("Session 生命周期", "03_session_lifecycle_demo.py", "demo_session_lifecycle", demo03),
    ("DB Health", "04_db_health_demo.py + app/routers/health.py", "demo_db_health", demo04),
    ("Settings/.env", "app/config.py", "Settings", None),
]


def main() -> None:
    print("===== V27 concept_index =====")
    for name, location, func_name, module in CONCEPT_INDEX:
        if module is not None:
            func = getattr(module, func_name, None)
            assert callable(func), f"{location} 缺少 {func_name}()"
        print(f"{name} → {location} → {func_name}()")


if __name__ == "__main__":
    main()
