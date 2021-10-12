import json
from dataclasses import MISSING
from hashlib import blake2b
from typing import Any, Coroutine, Hashable, Optional

from fastapi_memory_cache.constants import CORO_RETURN_TYPE
from fastapi_memory_cache.core import CachedValue, get_request_id, memory_cache
from fastapi_memory_cache.exceptions import UnhashableArgumentsException


def _generate_signature_key(signature: dict[Any, Any]) -> str:
    try:
        return blake2b(json.dumps(signature, sort_keys=True)).hexdigest()
    except Exception as e:
        raise UnhashableArgumentsException() from e


class MemoryCacheContext:

    coro: Coroutine[Any, Any, CORO_RETURN_TYPE]
    key: Optional[Hashable]

    def __init__(self, coro: Coroutine[Any, Any, CORO_RETURN_TYPE], key: Optional[Hashable] = None):
        self.coro = coro
        self.key = key

    async def get(self) -> CORO_RETURN_TYPE:

        request_id = get_request_id()

        if request_id is MISSING:

            return await self.coro

        else:
            request_cache = memory_cache.get(request_id)

            if not request_cache:
                request_cache = {}
                memory_cache[request_id] = request_cache

            cache_key = self.key or _generate_signature_key(self.coro.cr_frame.f_locals)

            cached_value = request_cache.get(cache_key)

            if cached_value:
                return cached_value.data

            value = await self.coro
            request_cache[cache_key] = CachedValue(data=value)

            return value
