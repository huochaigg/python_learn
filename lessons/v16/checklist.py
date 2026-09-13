"""V16 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v16/checklist.py
建议先自己答，再对照 app/main.py、models.py、Swagger /docs。
"""

QUESTIONS = [
    "1. FastAPI 为什么能知道 user_id 是 Path Parameter，而不是 Query？",
    "2. GET /users 里 page: int = 1 为什么会变成 Query？",
    "3. 为什么 user: UserCreate 会被识别成 Request Body，而不是 Query？",
    "4. keyword: str | None 是否一定 optional？和 keyword: str | None = None 差在哪？",
    "5. model_dump() 做什么？为什么现在不优先写 .dict()？",
    "6. uvicorn lessons.v16.app.main:app 里，冒号前面和后面分别指什么？",
    "7. FastAPI 路由写成 def 和 async def 都可以吗？什么时候才应该 async def？",
    "8. 普通 Python 函数里 age: int，传入字符串会怎样？FastAPI 接到无法转换的 Path 又会怎样？",
    "9. BaseModel 和 dataclass 各自更适合什么场景？",
    "10. Annotated[int, Query(ge=1)] 里，int 和 Query(...) 分别扮演什么角色？",
    "11. Path() 和 Query() 约束的是哪一类 HTTP 参数？Field() 约束的是什么？",
    "12. /docs、/redoc、/openapi.json 分别是什么？它们从哪里来的信息？",
    "13. 访问 /users/abc 或 POST 缺少 name 时，你预期看到什么状态码？要不要现在自己写校验 if？",
    "14. @app.get 和 NestJS @Get 都是装饰器。相似点是什么？为什么不能当成同一个东西？",
    "15. fastapi dev 和 uvicorn module:app --reload 是什么关系？开发时优先用哪个？",
]


def main() -> None:
    print("===== V16 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v16 checklist 运行完毕 ---")
