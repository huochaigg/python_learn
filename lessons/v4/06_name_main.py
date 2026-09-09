"""V4-06 __name__ 与 if __name__ == "__main__":。

学习目标：
1. 看懂模块的 __name__ 在「直接运行」和「被 import」时分别是什么。
2. 知道 __main__ 表示当前模块作为程序入口。
3. 会用 if __name__ == "__main__": 包住入口逻辑。

运行：
  uv run python lessons/v4/06_name_main.py
  uv run python lessons/v4/greeter.py
  uv run python lessons/v4/import_greeter.py
"""

from pathlib import Path
import subprocess
import sys

print("06_name_main.py 自己的 __name__ =", __name__)

# 导入 greeter：它的顶层 print 会执行，但 if __name__ == "__main__" 里的 main() 不会。
import greeter

print("导入之后 greeter.__name__ =", greeter.__name__)
print("复用 greeter.greet =", greeter.greet("Lucy"))

print("\n--- 直接运行 greeter.py，它的 __name__ 会变成 __main__ ---")
sys.stdout.flush()
greeter_path = Path(__file__).resolve().parent / "greeter.py"
subprocess.run([sys.executable, str(greeter_path)], check=True)

print("\n--- 运行辅助文件 import_greeter.py ---")
sys.stdout.flush()
importer_path = Path(__file__).resolve().parent / "import_greeter.py"
subprocess.run([sys.executable, str(importer_path)], check=True)


def main() -> None:
    """本课自己的入口，演示同样的写法。"""
    print("06 的 main() 只在直接运行本文件时执行")


if __name__ == "__main__":
    main()
    print("\n--- 06 __name__ / __main__ 运行完毕 ---")

# 本文件重点：
# 1. 直接运行时 __name__ == "__main__"；被 import 时 __name__ 通常是模块名。
# 2. if __name__ == "__main__": 用来区分这两种情况。
# 3. 模块既可以当库被 import，也可以自己跑 main() 做快速试验。
# 4. 你前面每课文件末尾那句，就是这个机制。
