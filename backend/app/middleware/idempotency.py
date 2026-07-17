"""Idempotency middleware – enforces X‑Idempotency‑Key.

Behavior (per DATA_GOVERNANCE.md §11):
  * Header required for POST/PATCH/DELETE.
  * Store key → response payload (JSON) in Redis for 24 h.
  * If duplicate key with same payload → replay stored response.
  * If duplicate key with *different* payload → raise IdempotencyConflict (409).
"""

from __future__ import annotations

import json
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.dependencies import get_redis, settings


class IdempotencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        method = request.method.upper()
        if method not in {"POST", "PATCH", "DELETE"}:
            return await call_next(request)

        key = request.headers.get("X-Idempotency-Key")
        if not key:
            # Header missing – reject per contract
            from app.exceptions import IdempotencyConflict

            raise IdempotencyConflict(detail="X-Idempotency-Key header wajib untuk operasi ini")

        # Simple validation – UUID v4 pattern (we accept any non‑empty string for now)
        async for redis in get_redis():
            cached = await redis.get(key)
            if cached:
                # Key exists – compare bodies
                body = await request.body()
                if body and body != cached.encode():
                    from app.exceptions import IdempotencyConflict

                    raise IdempotencyConflict(
                        detail="X-Idempotency-Key sudah dipakai dengan payload berbeda"
                    )
                # Replay stored response (assume JSON stored)
                data = json.loads(cached)
                return JSONResponse(content=data)
            # No existing key – proceed and store after response
            response = await call_next(request)
            # Capture response body (must be JSON serializable)
            if isinstance(response, JSONResponse):
                payload = response.body.decode()
                await redis.setex(
                    key, settings.IDEMPOTENCY_TTL_SECONDS, payload
                )
            return response
        # Should never get here – fallback error
        return Response(status_code=500, content="Idempotency middleware broken")
