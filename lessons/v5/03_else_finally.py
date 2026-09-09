"""V5-03 else 与 finally。

学习目标：
1. 知道 else 只在 try 没抛异常时执行。
2. 知道 finally 无论成功失败通常都会执行。
3. 能把「读取成功后再处理」和「最后一定清理」拆开写。

运行：uv run python lessons/v5/03_else_finally.py
"""

raw_users = [
    '{"name": "Tom", "age": 31}',
    "not-json",
]


def fake_parse(raw: str) -> dict[str, str | int]:
    """假装解析用户数据。非法文本就抛 ValueError。"""
    if raw.startswith("{") and "name" in raw and "age" in raw:
        # 刻意写死，避免本课引入 json 细节。
        if "Tom" in raw:
            return {"name": "Tom", "age": 31}
    raise ValueError(f"invalid payload: {raw}")


# ---------------------------------------------------------------------------
# else：只有 try 整段成功（没异常）才执行。
# 什么时候用：把「成功之后的后续处理」和「可能失败的读取」分开。
# JS/TS 对比：JS 没有同级 else；成功逻辑通常直接写在 try 末尾。
# 注意：不是每个 try 都要写 else，知道语义即可。
#
# finally：无论 try 成功还是 except 接住了，通常都会执行。
# 什么时候用：关文件、释放连接、清理临时状态。
# JS/TS 对比：≈ finally { ... }
# 注意：后续会学更推荐的 with / context manager，finally 先建立直觉。
# ---------------------------------------------------------------------------
for raw in raw_users:
    print(f"\n处理: {raw}")
    cleaned = False
    try:
        user = fake_parse(raw)
    except ValueError as e:
        print("  except: 读取失败 =", e)
    else:
        print("  else: 读取成功，继续处理 =", user)
    finally:
        cleaned = True
        print("  finally: 无论成败都做清理, cleaned =", cleaned)

# 再看一次「失败时 else 不会走」：
print("\n对照：失败路径")
try:
    fake_parse("bad")
    print("  try 成功")
except ValueError:
    print("  except 执行了")
else:
    print("  else 不会执行")
finally:
    print("  finally 一定执行")

if __name__ == "__main__":
    print("\n--- 03 else / finally 运行完毕 ---")

# 本文件重点：
# 1. try 成功 → else；try 失败 → except。
# 2. finally 通常无论成功失败都会跑，适合清理。
# 3. 成功后的业务处理可以放 else，让 try 只负责「可能失败的那一步」。
# 4. 资源释放后面更推荐 with，本课先记住 finally 的语义。
