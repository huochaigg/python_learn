"""模拟鉴权。不是 JWT / OAuth2 / 密码 Hash，只为看清 dependency chain。"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from lessons.v18.app.schemas.user import CurrentUser

_TOKENS: dict[str, CurrentUser] = {
    "user-token": CurrentUser(id=1, name="Tom", role="user"),
    "admin-token": CurrentUser(id=2, name="Ada", role="admin"),
}


def get_token(
    x_token: Annotated[str, Header(description="模拟 token：user-token 或 admin-token")],
) -> str:
    # 缺 Header 时 FastAPI 会按 Header 必填做校验（通常 422）。
    print("[dep] 1 get_token")
    if x_token not in _TOKENS:
        # HTTPException：让这次请求失败。不是 @app.exception_handler，统一错误体留给 V19。
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return x_token


def get_current_user(token: Annotated[str, Depends(get_token)]) -> CurrentUser:
    # Sub-dependency：dependency 里还可以再 Depends。FastAPI 会递归解析依赖树。
    # 本次请求会先跑 get_token，再跑这里。不是启动时平铺执行一遍。
    print("[dep] 2 get_current_user")
    return _TOKENS[token]


def require_admin(
    user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    print("[dep] 3 require_admin")
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin only")
    return user


def verify_request_header(
    x_client: Annotated[str, Header(description="演示用，固定填 v18-demo")],
) -> None:
    # 只执行检查，不需要把返回值注入 endpoint。适合放在 dependencies=[Depends(...) ]。
    print("[dep] verify_request_header")
    if x_client != "v18-demo":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="need X-Client: v18-demo")
