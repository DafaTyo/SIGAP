"""Rate‑limit middleware – token bucket per IP or user.

Configuration (from Settings):
  RATE_LIMIT_DEFAULT (requests per window)
  RATE_LIMIT_WINDOW_SECONDS (window size)

Implementation uses Redis INCR with TTL.
"""

from __future__ import annotations

import time
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.dependencies import get_redis, settings
from app.exceptions import RateLimitExceeded


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Identify key – prefer authenticated user, fallback to IP
        auth = request.state.user if hasattr(request.state, "user") else None
        identifier = auth.id if auth else request.client.host
        key = f"rl:{identifier}"

        async for redis in get_redis():
            # Increment counter atomically; set TTL if first hit
            current = await redis.incr(key)
            if current == 1:
                await redis.expire(key, settings.RATE_LIMIT_WINDOW_SECONDS)
            if current > settings.RATE_LIMIT_DEFAULT:
                raise RateLimitExceeded(
                    detail=f"Rate limit exceeded: {settings.RATE_LIMIT_DEFAULT} per {settings.RATE_LIMIT_WINDOW_SECONDS}s"
                )
            break
        return await call_next(request)
