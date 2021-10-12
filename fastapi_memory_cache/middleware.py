from dataclasses import MISSING

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from fastapi_memory_cache.core import ctx, memory_cache


class RequestMemoryCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = ctx.set(id(request))

        if request_id is not MISSING:
            memory_cache[request_id] = {}

        response = await call_next(request)
        ctx.reset(request_id)

        if request_id in memory_cache:
            del memory_cache[request_id]

        return response
