"""demo_package 的包入口。

__init__.py 是什么：
- 让这个目录被明确当成 package（学习阶段建议保留）。
- 可以什么都不写；也可以在这里重新导出常用名字，方便外部少写一层路径。

JS/TS 对比：有点像目录里的 index.ts 统一出口。
不是完全等价，但学习阶段这样记很有用。

下面这行是相对导入：从「当前包」里的 math_utils 拿出 add。
于是外部可以：from demo_package import add
而不必：from demo_package.math_utils import add
"""

from .math_utils import add
