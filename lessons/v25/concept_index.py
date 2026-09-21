"""
文件作用：V25 概念定位索引。只列出概念落在哪个文件/函数，不跑业务。
重点概念：UNIQUE、NOT NULL、CHECK、ForeignKey、IntegrityError、Idempotency-Key。
观察重点：回头查概念时先看这里，再打开对应 demo 函数。
"""

CONCEPT_INDEX = {
    "UNIQUE": "constraints_demo.py → demo_unique()",
    "NOT NULL": "constraints_demo.py → demo_not_null()",
    "CHECK": "constraints_demo.py → demo_check_constraint()",
    "ForeignKey完整性": "constraints_demo.py → demo_foreign_key()",
    "IntegrityError": "integrity_error_demo.py → demo_integrity_error_flow()",
    "忘记rollback": "integrity_error_demo.py → demo_forgot_rollback()",
    "先查不是并发保证": "race_unique_demo.py → main()",
    "幂等": "idempotency_demo.py → create_order_idempotent() / demo_same_key()",
    "Idempotency-Key": "idempotency_demo.py → demo_same_key() / routers/orders.py create_order()",
    "三层校验": "constraint_vs_validation_demo.py → demo_three_layers()",
}


def main() -> None:
    print("===== V25 concept_index =====")
    for name, loc in CONCEPT_INDEX.items():
        print(f"{name} → {loc}")


if __name__ == "__main__":
    main()
    print("--- v25 concept_index 运行完毕 ---")
