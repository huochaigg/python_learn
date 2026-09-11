"""V11-02 闭包：inner 记住 outer 的变量。

学习目标：
1. 看懂 outer 返回 inner，inner 仍能读外层变量。
2. 知道 outer 执行结束后，这些变量不会立刻丢掉。
3. 能对应到 JavaScript closure，但不深入 cell/字节码。

运行：uv run python lessons/v11/02_closure.py
"""


def make_multiplier(n: int):
    # 闭包 Closure：inner 引用了外层的 n。
    # 用途：把配置（这里是 n）「包进」以后要调用的函数里。
    # 执行时机：make_multiplier(10) 结束之后，n 仍然被 inner 握着。
    # JS/TS 对比：function makeMultiplier(n) { return (x) => n * x }
    def inner(x: int) -> int:
        return n * x

    return inner


times10 = make_multiplier(10)
times3 = make_multiplier(3)
print("times10(2) =", times10(2))
print("times3(2) =", times3(2))
print("两个闭包各自记住自己的 n，互不影响")

# Decorator 里的 wrapper 也常形成闭包：记住被装饰的 func，以及 decorator 的配置。

if __name__ == "__main__":
    print("\n--- 02 闭包 运行完毕 ---")

# 本文件重点：
# 1. inner 可以捕获 outer 的变量，这就是闭包。
# 2. outer 返回后，那些变量仍然活在 inner 上。
# 3. 和 JS closure 是同一类能力。
# 4. 后面 wrapper 记住 func / role / times，靠的就是闭包。
