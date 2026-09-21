"""
文件作用：对照三层校验，避免把 Pydantic / Service / 数据库约束混成一件事。
重点概念：请求结构校验、业务规则、数据库最终完整性。
观察重点：Pydantic 拦类型/缺字段；Service 拦「email 已存在」体验；UNIQUE 拦并发漏网。
"""

from pydantic import ValidationError

from lessons.v25.app.schemas.order import UserCreate


def demo_pydantic_layer() -> None:
    print("\n===== Pydantic / FastAPI：请求结构 =====")
    try:
        UserCreate(name="", email="a@b.com")
    except ValidationError as extra:
        print("empty name blocked before database:", extra.error_count(), "error(s)")


def demo_three_layers() -> None:
    print(
        """
===== three layers =====
1. Pydantic/FastAPI validation : 字段类型、必填、长度。拦坏请求，不保证库里唯一。
2. Service validation          : 业务规则（email 已存在则友好 409）。改善体验，不是并发保证。
3. Database constraint         : UNIQUE/NOT NULL/CHECK/FK。最后一道数据完整性防线。

不要因为已经有 Pydantic/Service 就删掉数据库约束。
"""
    )


def main() -> None:
    demo_three_layers()
    demo_pydantic_layer()


if __name__ == "__main__":
    main()
    print("\n--- v25 constraint_vs_validation_demo 运行完毕 ---")
