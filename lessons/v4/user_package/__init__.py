"""user_package 统一出口。

外部可以：
  from user_package import format_name, is_valid_name
而不必记住它们分别在哪个子模块。
"""

from .formatter import format_name
from .validator import is_valid_name
