"""V18 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v18/checklist.py
建议先自己答，再对照 dependencies/、终端 print、http://127.0.0.1:8001/docs。
"""

QUESTIONS = [
    "1. Depends(get_pagination) 为什么不能写成 Depends(get_pagination())？",
    "2. get_pagination 的返回值最后出现在哪里？谁在什么时候调用它？",
    "3. Annotated[PaginationParams, Depends(get_pagination)] 里，类型和 Depends 各干什么？",
    "4. dependency 函数里再写 Depends(get_token)，FastAPI 会怎么处理？",
    "5. 为什么 Python class 可以作为 dependency？endpoint 拿到的是什么？",
    "6. Annotated[CommonQueryParams, Depends()] 这种简写在说什么？",
    "7. yield 前、yield 出去、yield 后（finally）分别在什么时机执行？",
    "8. endpoint 抛异常时，为什么 Session 仍然应该 close？cleanup 能不能依赖正常 return？",
    "9. async def + yield 的 dependency 和 V14 Async Context Manager 有什么相似处？",
    "10. Depends 默认 use_cache 是什么？缓存活多久、活在哪一层？",
    "11. 为什么不能把 use_cache=True 理解成 Redis，也不能理解成 NestJS Singleton Provider？",
    "12. 同一 endpoint 多个子依赖都 Depends(get_request_marker) 时，默认会执行几次？",
    "13. Router/path 的 dependencies=[Depends(verify_xxx)] 和参数里的 Depends 差在哪？什么场景用前者？",
    "14. FastAPI Depends 和 NestJS constructor injection 最大的区别是什么（生命周期/计算时机）？",
    "15. get_pagination 里的 Query(ge=1) 为什么会出现在 Swagger 里，即使 endpoint 没直接声明 page？",
    "16. 本课 X-Token 是真 JWT 吗？真实 Auth 应该放在哪一版再做？",
]


def main() -> None:
    print("===== V18 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v18 checklist 运行完毕 ---")
