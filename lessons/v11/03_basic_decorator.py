"""V11-03 最简单的 decorator：接收函数，返回新函数。

学习目标：
1. 手写 log_execution(func) → wrapper → 调用原函数。
2. 通过打印看清：包装发生在定义时，日志发生在调用时。
3. 记住一句话：装饰器本质上是「接收函数并返回新函数的函数」。

运行：uv run python lessons/v11/03_basic_decorator.py
"""


def log_execution(func):
    # Decorator：输入一个函数 func，返回一个新函数 wrapper。
    print(f"[定义阶段] 正在装饰 {func.__name__}")

    def wrapper():
        print("[调用阶段] wrapper 之前")
        func()
        print("[调用阶段] wrapper 之后")

    return wrapper


def hello() -> None:
    print("[调用阶段] hello 函数体")


print("手动装饰：hello = log_execution(hello)")
hello = log_execution(hello)
print("装饰已经完成，hello 现在其实是 wrapper")
print("开始真正调用 hello()")
hello()

if __name__ == "__main__":
    print("\n--- 03 基础 decorator 运行完毕 ---")

# 本文件重点：
# 1. Decorator = 接收函数并返回新函数。
# 2. log_execution(hello) 发生在定义/装饰阶段。
# 3. 真正调用时跑的是 wrapper，再进原函数。
# 4. 本课 wrapper 还没处理参数和返回值，下一课补语法糖。
