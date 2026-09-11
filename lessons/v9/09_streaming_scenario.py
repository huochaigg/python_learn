"""V9-09 同步流式 Demo：chunk 边产边消费。

学习目标：
1. 对比「拼完再 return」和「yield 一个 chunk」。
2. 理解这和 FastAPI StreamingResponse / SSE / AI token streaming 是同一类思想。
3. 本课不发真实网络请求，也不安装 FastAPI。

运行：uv run python lessons/v9/09_streaming_scenario.py
"""


def complete_message() -> str:
    """普通方案：等全部 chunk 到齐，拼成完整字符串再返回。"""
    chunks = ["Hello", " ", "Python", " ", "Agent"]
    text = "".join(chunks)
    print("  complete_message 一次返回整句")
    return text


def stream_message():
    """流式方案：有一个 chunk 就 yield 一个，调用方立刻能看到。"""
    chunks = ["Hello", " ", "Python", " ", "Agent"]
    for chunk in chunks:
        print(f"  产出 chunk: {chunk!r}")
        yield chunk


print("一次性 return:")
print("  最终 =", complete_message())

print("\n流式 yield（调用端 for 消费）:")
pieces: list[str] = []
for chunk in stream_message():
    pieces.append(chunk)
    print("  调用端此刻已收到 =", "".join(pieces))

print("最终拼起来同样是 =", "".join(pieces))

# 以后 FastAPI 里可能看到类似：
#   StreamingResponse(stream_message())
# 思想就是：Generator 不断产出数据，框架边收边发给客户端。
# SSE / Agent token streaming 也是「来一块 yield 一块」，而不是等全文结束。
# V9 只学同步 Generator；async def + yield 形成的 Async Generator 留到后面。

if __name__ == "__main__":
    print("\n--- 09 流式场景 运行完毕 ---")

# 本文件重点：
# 1. return 整句要等全部算完；yield chunk 可以边生成边给下游。
# 2. 这就是 streaming 的同步版缩影。
# 3. FastAPI StreamingResponse / SSE / Agent streaming 会继续用这个思想。
# 4. 本课没有真的 HTTP，先把 Generator 流跑顺。
