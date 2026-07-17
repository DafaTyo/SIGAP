"""Redis singleton client for idempotency, rate-limit, and caching.

References:
  - dependencies/TASK.md: singleton client, DI via Depends
  - DATA_GOVERNANCE.md §11: idempotency keys TTL 24h
"""

from __future__ import annotations

from collections.abc import AsyncGenerator

import redis.asyncio as aioredis

from app.core.config import settings

_redis_client: aioredis.Redis | None = None


def _get_client() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis_client


async def get_redis() -> AsyncGenerator[aioredis.Redis, None]:
    """Yield the Redis client for DI."""
    yield _get_client()
