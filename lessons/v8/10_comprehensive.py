"""V8-10 综合练习：三种方法、property/setter、dataclass、field、__post_init__。

学习目标：
1. 把本版 API 串到一个小商品/购物车场景里。
2. 先 TODO，再对照示例答案。
3. 选方法时反复用：要实例 → 实例方法；要类/工厂 → classmethod；都不依赖 → staticmethod。

运行：uv run python lessons/v8/10_comprehensive.py

用法：
- 每个练习的 TODO 留白给你写。
- 示例答案会一起运行，方便对照。
- 若只想跑自己的代码，把对应「示例答案」暂时注释掉即可。
"""

from dataclasses import dataclass, field


# =============================================================================
# 练习 1
# TODO: 写 dataclass Product，字段 name: str、unit_price: int、
#       tags: list[str] = field(default_factory=list)。
#       在 __post_init__ 里：name strip；unit_price < 0 则 raise ValueError。
# =============================================================================
print("\n===== 练习 1 TODO =====")


print("===== 练习 1 示例答案 =====")


@dataclass
class Product:
    name: str
    unit_price: int
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.name = self.name.strip()
        if self.unit_price < 0:
            raise ValueError("unit_price must be >= 0")

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return len(name.strip()) >= 2

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(name=data["name"], unit_price=data["unit_price"])

    @property
    def label(self) -> str:
        return f"{self.name} price={self.unit_price}"


book = Product("  Python Book  ", 50)
print("book =", book)
print("book.tags 默认是新 list =", book.tags)
try:
    Product("x", -1)
except ValueError as e:
    print("__post_init__ 校验 =", e)


# =============================================================================
# 练习 2
# TODO: 给 Product 加 is_valid_name staticmethod、from_dict classmethod、
#       label property。用 from_dict 建一个商品并打印 label。
# =============================================================================
print("\n===== 练习 2 TODO =====")


print("===== 练习 2 示例答案 =====")
print("is_valid_name('A') =", Product.is_valid_name("A"))
pen = Product.from_dict({"name": "Pen", "unit_price": 8})
print("from_dict label =", pen.label)
pen.tags.append("stationery")
print("pen.tags =", pen.tags, "book.tags 不受影响 =", book.tags)


# =============================================================================
# 练习 3
# TODO: 写普通 class CartLine，__init__(product, qty)。
#       qty 用 getter/setter，qty <= 0 时 raise ValueError。
#       再写 property subtotal = unit_price * qty。
# =============================================================================
print("\n===== 练习 3 TODO =====")


print("===== 练习 3 示例答案 =====")


class CartLine:
    def __init__(self, product: Product, qty: int) -> None:
        self.product = product
        self.qty = qty

    @property
    def qty(self) -> int:
        return self._qty

    @qty.setter
    def qty(self, value: int) -> None:
        if value <= 0:
            raise ValueError("qty must be > 0")
        self._qty = value

    @property
    def subtotal(self) -> int:
        return self.product.unit_price * self.qty


line = CartLine(book, 2)
print("subtotal =", line.subtotal)
line.qty = 4
print("改 qty 后 subtotal =", line.subtotal)
try:
    line.qty = 0
except ValueError as e:
    print("setter =", e)


print("---------- 处理结果 ----------")
print(book.label, book.tags)
print(pen.label, pen.tags)
print("line.qty =", line.qty, "subtotal =", line.subtotal)

if __name__ == "__main__":
    print("\n--- 10 综合练习 运行完毕 ---")

# 本文件重点：
# 1. dataclass + __post_init__ 做构造后校验；可变字段用 default_factory。
# 2. from_dict 用 classmethod + cls(...)；纯校验用 staticmethod。
# 3. label / subtotal 是计算属性，访问不加括号。
# 4. setter 内存 _qty，非法值 raise。
