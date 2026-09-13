"""小型订单处理服务（纯 Python，无 FastAPI / 无数据库）。

分层对应 NestJS 的大致映射：
- models      ≈ DTO / Entity
- repositories ≈ Repository
- services    ≈ Service
- exceptions  ≈ 业务异常
- utils       ≈ 横切工具（decorator）
- main        ≈ Bootstrap
"""
