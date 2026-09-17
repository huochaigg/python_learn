"""V19 速查：异常与统一错误响应。

运行：uv run python lessons/v19/notes.py
"""

NOTES = """
HTTPException
  HTTP 层错误：status_code / detail / headers。raise 后进框架异常流程。
  不要 return {"error": ...} 假装失败（那通常还是 200）。
  NestJS ≈ throw new HttpException。

BizException
  业务错误语义（code / message / status_code），不是 Response。
  Service 抛它；handler 再映射 HTTP。子类可共用基类 handler。

exception_handler
  注册「某类异常 → Response」。类似 Nest ExceptionFilter。
  JSONResponse 显式写 status + JSON。不要把 Exception 对象或 traceback 给前端。

RequestValidationError
  Path/Query/Body 校验失败，框架在进 endpoint 前抛。
  exc.errors() 拿 loc/type/msg。HTTP 保持 422，只统一 body。
  不是业务 400/404。

Validation vs Business
  422 = 请求形状不对。
  400/404/409 = 请求形状对，但业务不允许（状态非法 / 不存在 / 库存不足）。

全局 Exception handler
  只接没被更具体 handler 接住的未知异常。
  客户端：500 + 通用文案。服务端：logging.exception 记 traceback。

业务 code vs HTTP status
  code 给前端分支（USER_NOT_FOUND）。
  status_code 走 HTTP 语义。统一 JSON ≠ 全部改成 200。

raise ... from e
  保留因果链给日志；客户端仍只看到业务 JSON。
"""

if __name__ == "__main__":
    print(NOTES)
    print("--- v19 notes 运行完毕 ---")
