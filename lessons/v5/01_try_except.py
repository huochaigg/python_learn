"""V5-01 基础 try / except。

学习目标：
1. 知道运行出错会抛异常，不是静默失败。
2. 会用 try / except 捕获，并拿到异常对象 e。
3. 能把 Python 异常对应到 JS 的 try/catch。

运行：uv run python lessons/v5/01_try_except.py
"""

# ---------------------------------------------------------------------------
# 异常：运行时出错时抛出的对象。不处理就会中断当前流程，把错误往上传播。
# JS/TS 对比：Python Exception ≈ JavaScript Error
# ---------------------------------------------------------------------------

# ZeroDivisionError：除以 0。
# 触发场景：数字运算里除数为 0。
print("10 / 2 =", 10 / 2)

try:
    result = 10 / 0
    print("这行不会执行，因为上一行已经抛异常")
except ZeroDivisionError as e:
    # except：try 里抛出「这个类型」的异常时才进来。
    # as e：把异常对象绑到变量 e，方便打印/记录。
    # JS/TS 对比：catch (error) { console.log(error) }
    print("捕获到 ZeroDivisionError =", type(e).__name__, e)

# ValueError：值的类型对，但内容不合法。
# 触发场景：int("abc")、把非法字符串转成数字等。
try:
    age = int("abc")
except ValueError as e:
    print("捕获到 ValueError =", e)

# 注意：主示例不要写裸 except:。
# 裸 except 会连 KeyboardInterrupt 等也不放过，正式项目几乎不用。
# 错误示例（不要学）：
#   try:
#       int("abc")
#   except:
#       pass

if __name__ == "__main__":
    print("\n--- 01 try / except 运行完毕 ---")

# 本文件重点：
# 1. Python 异常 ≈ JS Error；try/except ≈ try/catch。
# 2. except SomeError as e 只处理这一类，e 是异常对象。
# 3. try 里一旦 raise/抛错，后面的正常代码不会再跑。
# 4. 不要用裸 except: 当主写法。
