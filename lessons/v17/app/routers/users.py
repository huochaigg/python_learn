"""用户接口。内存 dict 只为练 Router / Schema，不是数据层。"""

from typing import Any

from fastapi import APIRouter, status

from lessons.v17.app.schemas.user import UserCreate, UserPut, UserResponse, UserUpdate

# APIRouter：按业务域拆一组 Path Operation，而不是全部写在 main.py。
# NestJS 对照：职责上有点像 @Controller("users") 里那一组路由，但不是同一个模块/DI 机制。
# prefix：自动拼到本 Router 每条路径前面。这里 @router.get("") 最终是 GET /users。
# tags：主要给 OpenAPI/Swagger 分组，文档里会看到 users / orders 两栏。
router = APIRouter(prefix="/users", tags=["users"])

# 临时存储：进程内 dict + 自增 id。重启就没了。后续才拆 Service/Repository/数据库。
_users: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Ada",
        "email": "ada@example.com",
        "password": "secret",
    }
}
_next_id = 2


@router.get("/demo/bad-response", response_model=UserResponse)
def bad_response() -> dict[str, str]:
    # 可选 Demo：故意缺 id/email，触发服务端 Response Validation Error。
    # 主流程不会调用它。Request 校验失败 ≈ 客户端数据不对（通常 422）；
    # Response 校验失败 ≈ 后端自己违反了响应契约（通常 500）。
    return {"name": "broken"}


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user: UserCreate) -> dict[str, Any]:
    # response_model=UserResponse：不只是 Swagger 文档。
    # 还会按这个模型校验响应、序列化 JSON，并过滤模型里没有的字段（这里滤掉 password）。
    # 和返回类型 annotation 同时写时，FastAPI 以 response_model 作为主要响应模型配置。
    # 常见坑：把过滤当成唯一安全措施。正式项目本身就不该无意义传递/记录明文密码。
    # NestJS 对照：有点像 ClassSerializerInterceptor + @Exclude，机制不同。
    #
    # status.HTTP_201_CREATED：语义化状态码常量，值仍是 201，比直接写 201 好读。
    # from fastapi import status 拿到的就是这一组常量。
    global _next_id
    saved = {"id": _next_id, **user.model_dump()}
    _users[_next_id] = saved
    _next_id += 1
    return saved


@router.get("")
def list_users() -> list[UserResponse]:
    # 用返回类型 annotation 声明响应模型：list[UserResponse]。
    # Swagger 会显示 UserResponse 数组；每个元素同样不会带 password。
    return list(_users.values())


@router.get("/{user_id}")
def get_user(user_id: int) -> UserResponse:
    # 只写 -> UserResponse，不写 response_model=。和 POST 那条对照两种声明方式。
    user = _users.get(user_id)
    if user is None:
        # TODO: 后续异常处理版本改成 HTTPException(status_code=404)
        return UserResponse(id=user_id, name="placeholder", email="missing@example.com")
    return user


@router.patch("/{user_id}")
def patch_user(user_id: int, user_update: UserUpdate) -> UserResponse:
    current = _users.get(user_id)
    if current is None:
        # TODO: 后续异常处理版本改成 HTTPException(status_code=404)
        return UserResponse(id=user_id, name="placeholder", email="missing@example.com")
    # model_dump(exclude_unset=True)：只导出客户端真正提交过的字段。
    # UserUpdate 里 name/email 都有默认 None；如果原样 dump，没传的 email 会变成 None，
    # 再 update 就会把原来的 email 盖掉。exclude_unset=True 专门避开这个坑，适合 PATCH。
    patch = user_update.model_dump(exclude_unset=True)
    current.update(patch)
    return current


@router.put("/{user_id}")
def put_user(user_id: int, user_put: UserPut) -> UserResponse:
    # PUT 通常偏向完整替换资源；PATCH 偏向部分修改。
    # 真实公司 API 约定可能不同，本课按标准 REST 语义学。
    # 这里要求 name、email 都传；没出现在 Body 里的 password 保持原值。
    current = _users.get(user_id)
    if current is None:
        # TODO: 后续异常处理版本改成 HTTPException(status_code=404)
        return UserResponse(id=user_id, name="placeholder", email="missing@example.com")
    current.update(user_put.model_dump())
    return current


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> None:
    # 204 No Content：成功但没有响应体。不要再 return 一坨 JSON。
    _users.pop(user_id, None)
    return None