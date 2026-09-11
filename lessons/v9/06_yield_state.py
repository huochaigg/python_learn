"""V9-06 yield 的暂停与恢复：局部变量和执行位置都会被记住。

学习目标：
1. 通过日志看清：第一次 next 跑到第一个 yield 就停。
2. 第二次 next 从暂停处继续，不会重头执行函数。
3. 确认生成器会保存局部变量。

运行：uv run python lessons/v9/06_yield_state.py
"""


def numbered_chunks():
    n = 0
    print("准备生成 1")
    n += 1
    yield n
    print("yield 1 后恢复执行")

    print("准备生成 2")
    n += 1
    yield n
    print("yield 2 后恢复执行")

    print("准备生成 3")
    n += 1
    yield n
    print("yield 3 后函数即将结束")


gen = numbered_chunks()
print("=== 第一次 next ===")
print("拿到 =", next(gen))
print("=== 第二次 next ===")
print("拿到 =", next(gen))
print("=== 第三次 next ===")
print("拿到 =", next(gen))
print("=== 第四次 next：函数彻底结束 ===")
try:
    next(gen)
except StopIteration:
    print("StopIteration")

print("\n同一个 generator object 消费完后再 for，不会有新数据:")
print("list(gen) =", list(gen))
print("要重新来一遍，必须再调用 numbered_chunks() 创建新对象")

if __name__ == "__main__":
    print("\n--- 06 yield 状态 运行完毕 ---")

# 本文件重点：
# 1. next 执行到 yield 就暂停；下一次从暂停点继续。
# 2. 局部变量（这里的 n）会跟着生成器一起活着。
# 3. 一个 generator object 通常只能消费一次。
# 4. Generator Function 可以反复调用，每次得到新的 Generator Object。
