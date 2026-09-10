"""V6-07 后端小场景：读配置 → 修改 → 存回 JSON。

学习目标：
1. 把 Path、with、json、V5 异常处理拼在一起。
2. 文件不存在时给出合理默认配置。
3. JSON 格式错误时捕获 json.JSONDecodeError。

运行：uv run python lessons/v6/07_backend_scenario.py
"""

from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parent / "data"
CONFIG = DATA_DIR / "config.json"
BROKEN = DATA_DIR / "broken.json"
MISSING = DATA_DIR / "missing-config.json"


def load_config(path: Path) -> dict:
    """读取 JSON 配置。文件不存在则返回默认值，不直接崩。"""
    if not path.exists():
        print(f"  {path.name} 不存在，使用默认配置")
        return {"app": "python-learn", "debug": False, "port": 8000}

    with path.open("r", encoding="utf-8") as file:
        # json.load：从文件对象读 JSON。
        # 非法内容会抛 json.JSONDecodeError（JSONDecodeError 是 ValueError 的子类）。
        return json.load(file)


def save_config(path: Path, data: dict) -> None:
    """用 with 写回，避免漏关文件。"""
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


print("1) 读取现有 config.json")
config = load_config(CONFIG)
print("   当前 =", config)

print("2) 修改 debug / port 并保存")
config["debug"] = True
config["port"] = 9000
save_config(CONFIG, config)
reloaded = load_config(CONFIG)
print("   保存后再读 =", reloaded)

print("3) 缺失文件")
print("   missing =", load_config(MISSING))

print("4) 损坏的 JSON")
try:
    load_config(BROKEN)
except json.JSONDecodeError as e:
    print("   JSONDecodeError =", e)

if __name__ == "__main__":
    print("\n--- 07 后端场景 运行完毕 ---")

# 本文件重点：
# 1. 配置读写：Path 定位，with 管文件，json load/dump 负责序列化。
# 2. 文件不存在可以给默认值；坏 JSON 要捕 JSONDecodeError。
# 3. 这是 V5 异常处理 + V6 资源管理的典型组合。
# 4. 改完记得写回，否则只改了内存里的 dict。
