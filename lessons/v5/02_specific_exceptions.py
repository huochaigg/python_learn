"""V5-02 捕获具体异常：多个 except、组合捕获、最后才兜底。

学习目标：
1. 分清 ValueError / TypeError / KeyError 各自什么时候出现。
2. 会写多个 except 分支，以及 except (A, B) as e。
3. 记住：先具体，最后才可能 Exception；不要无脑吞掉。

运行：uv run python lessons/v5/02_specific_exceptions.py
"""


def parse_age(raw: str) -> int:
    """把输入转成年龄整数。内容不合法时抛 ValueError。"""
    return int(raw)


user = {"name": "Tom"}

# ---------------------------------------------------------------------------
# 多个 except：不同异常走不同处理。
# 匹配顺序从上到下，命中一个就停。
# JS/TS 对比：JS 一个 catch 后自己 if (error instanceof ...)；
# Python 可以直接按类型分流。
# ---------------------------------------------------------------------------
for raw in ["20", "abc"]:
    try:
        print(f"parse_age({raw!r}) =", parse_age(raw))
    except ValueError as e:
        # ValueError：类型大致对，值不合法。int("abc") 就是它。
        print(f"  ValueError: {e}")

try:
    # TypeError：操作和类型不匹配。len(123) 就是它。
    print("len(123) =", len(123))
except TypeError as e:
    print("  TypeError:", e)

# KeyError：dict 里没有这个键，还用 [] 去取。
# 触发场景：user["missing"]；user.get("missing") 不会抛。
try:
    print(user["city"])
except KeyError as e:
    print("KeyError，缺的键是", e)

# ---------------------------------------------------------------------------
# 一次捕获多种：这几种用同一套处理逻辑时才合并。
# ---------------------------------------------------------------------------
try:
    parse_age("abc")
except (ValueError, TypeError) as e:
    print("ValueError 或 TypeError 统一处理 =", type(e).__name__, e)

try:
    len(123)
except (ValueError, TypeError) as e:
    print("ValueError 或 TypeError 统一处理 =", type(e).__name__, e)

# ---------------------------------------------------------------------------
# Exception：大多数业务异常的基类，相当于比较大的兜底。
# 用途：最后记日志 / 返回统一失败，避免进程直接崩。
# 坑：太早 except Exception 会把本该暴露的 bug 藏起来。
# 正确顺序：具体异常 → 业务异常 → 最后才 Exception。
# ---------------------------------------------------------------------------
try:
    parse_age("abc")
except ValueError as e:
    print("先抓住具体的 ValueError =", e)
except Exception as e:
    print("这行只在「不是 ValueError 的其他 Exception」时才会到 =", e)

# 错误示例 1：except: pass 会吞掉所有问题，包括你没预料到的 bug。
#   try:
#       risky()
#   except:
#       pass
#
# 错误示例 2：到处都 except Exception，真实错误被统一成「失败了」。
#   try:
#       risky()
#   except Exception:
#       return None

if __name__ == "__main__":
    print("\n--- 02 具体异常 运行完毕 ---")

# 本文件重点：
# 1. 优先捕获具体类型：ValueError / TypeError / KeyError。
# 2. 多个 except 按类型分流；同类处理可用 except (A, B)。
# 3. except Exception 只适合最终兜底，不要当第一选择。
# 4. 不要 except: pass，也不要所有地方统一 except Exception。
