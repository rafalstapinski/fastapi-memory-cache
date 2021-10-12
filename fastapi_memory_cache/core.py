from contextvars import ContextVar
from dataclasses import _MISSING_TYPE, MISSING, dataclass
from typing import Any, Hashable

from fastapi_memory_cache.constants import CONTEXT_KEY

ctx: ContextVar[int | _MISSING_TYPE] = ContextVar(CONTEXT_KEY, default=MISSING)
memory_cache: dict[int, dict[Hashable, "CachedValue"]] = {}


@dataclass
class CachedValue:
    data: Any


def get_request_id() -> int | _MISSING_TYPE:
    return ctx.get()
