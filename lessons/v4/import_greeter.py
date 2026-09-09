"""辅助文件：只负责 import greeter，观察它不会自动执行 main()。

运行：uv run python lessons/v4/import_greeter.py
"""

import greeter

print("import_greeter.py 自己的 __name__ =", __name__)
print("被导入的 greeter.__name__ =", greeter.__name__)
print("可以复用函数：", greeter.greet("Tom"))
print("注意：上面没有自动调用 greeter.main()")
