"""V11-04 @decorator 语法糖。

学习目标：
1. 看懂 hello = log_execution(hello) 和 @log_execution 本质等价。
2. 再次区分：装饰动作 vs 真正调用。
3. 能和 NestJS 的 @Get 做概念对比，但知道底层机制不同。

运行：uv run python lessons/v11/04_decorator_syntax.py
"""


def log_execution(func):
    print(f"[定义阶段] @ 正在装饰 {func.__name__}")

    def wrapper():
        print("[调用阶段] 进入 wrapper")
        func()
        print("[调用阶段] 离开 wrapper")

    return wrapper


print("=== 手动版本 ===")


def ping() -> None:
    print("ping")


ping = log_execution(ping)
print("手动装饰结束，即将调用")
ping()

print("\n=== @ 语法糖，等价于 hello = log_execution(hello) ===")


@log_execution
def hello() -> None:
    print("hello")


print("函数定义结束，装饰已经发生")
print("即将调用 hello()")
hello()

# NestJS 对比：@Controller / @Get 也是「在声明时给函数/类挂上额外行为」。
# 注意：Python decorator 和 TS decorator 底层机制并不相同，只是概念接近。

if __name__ == "__main__":
    print("\n--- 04 @ 语法糖 运行完毕 ---")

# 本文件重点：
# 1. @log_execution 写在函数上一行，等价于定义后再 func = log_execution(func)。
# 2. 模块加载到 def 时就会执行装饰动作。
# 3. 调用函数时才跑 wrapper 里的业务/日志。
# 4. 和 NestJS 装饰器是概念类比，不是同一套实现。
