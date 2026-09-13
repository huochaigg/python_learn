"""V15 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v15/checklist.py
建议：先自己写/说一遍，再回对应版本的课程文件核对。
"""

QUESTIONS = [
    "1. *args 和 **kwargs 分别收下什么？调用方该怎么传？",
    "2. 参数写成 name: str | None 是否等于可以省略这个参数？和 name: str | None = None 差在哪？",
    "3. yield 和 return 对函数类型、调用结果分别意味着什么？",
    "4. Coroutine 和 Task 有什么区别？为什么说 async 不等于自动并发？",
    "5. Semaphore 和 Lock 各解决什么问题？能不能互相替代？",
    "6. async with 要求对象实现什么协议？进入和离开时分别会发生什么？",
    "7. async def 里出现 yield 之后，调用得到的是什么？能不能直接 await 整个对象？",
    "8. dataclass 和 TypeScript interface 最大的运行时差别是什么？",
    "9. 为什么说 Python 类型标注不等于运行时校验？",
    "10. Repository 返回 Order | None，Service 返回 Order。谁负责 raise OrderNotFoundError？为什么？",
    "11. constructor 注入 Repository，和 FastAPI Depends / NestJS constructor injection 的相似点是什么？",
    "12. @log_execution 这类 decorator 为什么要用 functools.wraps？",
    "13. 用户、库存、物流三个查询互相独立时，为什么用 asyncio.gather 而不是依次 await？",
    "14. 同步 for 结束时抛什么？async for 结束时抛什么？普通 list 能不能 async for？",
    "15. 内存 dict Repository 和真正的数据库差在哪？Semaphore(3) 是不是任务队列？",
    "16. field(default_factory=list) 要解决的是哪个坑？",
    "17. inspect.iscoroutinefunction() 用来判断什么？Async Generator Function 该不该当成普通 coroutine 去 await？",
    "18. 捕获业务异常时，为什么不要写成 except Exception 或 except: pass？",
]


def main() -> None:
    print("===== V15 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v15 checklist 运行完毕 ---")
