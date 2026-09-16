"""V17 阶段自测。只放问题，不给答案。

运行：uv run python lessons/v17/checklist.py
建议先自己答，再对照 routers/、schemas/ 和 http://127.0.0.1:8001/docs。
"""

QUESTIONS = [
    "1. 为什么需要 APIRouter，而不是继续把所有接口写在 main.py？",
    "2. prefix=\"/users\" 和 @router.get(\"\") / @router.get(\"/{user_id}\") 最终 URL 分别是什么？",
    "3. include_router() 在什么时候执行？它会不会发出一次 HTTP 请求？",
    "4. tags=[\"users\"] 主要影响运行时路由，还是 OpenAPI/Swagger 展示？",
    "5. 为什么 UserCreate 不能直接拿来当 UserResponse？",
    "6. response_model 除了生成文档，还会对响应做什么？",
    "7. 函数写 -> UserResponse，和装饰器写 response_model=UserResponse，FastAPI 怎么用？两者同时存在时以谁为主？",
    "8. 内部 dict 里明明有 password，为什么 HTTP JSON 里看不到？这是不是唯一安全措施？",
    "9. str | None = None 里，类型和默认值各解决什么问题？",
    "10. model_dump(exclude_unset=True) 解决 PATCH 的哪个坑？",
    "11. PUT 和 PATCH 按 REST 语义各偏向什么？如果只提交 name，PUT 接口还要求 email 吗？",
    "12. status.HTTP_201_CREATED 和直接写 201 有什么差别？204 为什么不能再返回 JSON？",
    "13. Request validation 失败和 Response validation 失败，分别通常说明谁写错了？",
    "14. NestJS 的 Controller 注册，和 FastAPI 的 include_router，相似点在哪？为什么不能画等号？",
    "15. 现在的 _users dict 重启后会怎样？V17 为什么还不拆 Service/Repository？",
]


def main() -> None:
    print("===== V17 checklist（先自己答）=====")
    for item in QUESTIONS:
        print()
        print(item)
        print("TODO: 在这里用自己的话写答案")


if __name__ == "__main__":
    main()
    print("\n--- v17 checklist 运行完毕 ---")
