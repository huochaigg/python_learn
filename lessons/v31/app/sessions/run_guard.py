import asyncio


class ConversationRunGuard:
    """同一进程内，拒绝同一个 conversation_id 的第二个活动 Agent Run。

    asyncio.Lock / 这套 set 都不能跨进程、跨 Worker 生效。
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._active: set[str] = set()

    def is_active(self, conversation_id: str) -> bool:
        return conversation_id in self._active

    async def try_acquire(self, conversation_id: str) -> bool:
        async with self._lock:
            if conversation_id in self._active:
                return False
            self._active.add(conversation_id)
            return True

    async def release(self, conversation_id: str) -> None:
        async with self._lock:
            self._active.discard(conversation_id)


conversation_run_guard = ConversationRunGuard()
