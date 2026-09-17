"""V19 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v19/checklist.py
"""

QUESTIONS = [
    "1. 什么时候直接 raise HTTPException？什么时候用 BizException？",
    "2. Service 为什么不推荐直接依赖 FastAPI 的 HTTPException？",
    "3. exception_handler / add_exception_handler 注册的是什么？在哪一层生效？",
    "4. JSONResponse 和 endpoint return dict 有什么不同？",
    "5. RequestValidationError 是谁抛的？它和 UserNotFoundError 差在哪？",
    "6. 为什么校验失败要保持 422，而不是为了统一格式改成 200？",
    "7. exc.errors() 返回什么？统一 Response 里为什么只保留 location/message/type？",
    "8. UserNotFoundError 继承 BizException 后，为什么不用单独注册 handler？",
    "9. 给 InsufficientStockError 再注册一个更具体 handler，匹配时谁优先？",
    "10. 全局 Exception handler 为什么不能把 traceback 返回前端？详细错误放哪？",
    "11. raise UserNotFoundError(...) from e 对服务端和客户端分别意味着什么？",
    "12. raise HTTPException(...) 和 return {\"error\": \"...\"} 的 HTTP 语义差在哪？",
    "13. Router 里为什么不要每个 endpoint 都 try/except BizException？",
    "14. 为什么不要写成 except Exception: return None？",
    "15. NestJS ExceptionFilter / ValidationPipe / HttpException，分别大致对应 V19 的什么？",
    "16. 业务 code（USER_NOT_FOUND）和 HTTP 404 为什么要同时存在、而不是只留一个？",
]


def main() -> None:
    print("===== V19 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v19 checklist 运行完毕 ---")
