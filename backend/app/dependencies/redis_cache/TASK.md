# TASK‑BE‑007‑02 – Cache Dependency (Redis)

## Goals
- Provide a FastAPI dependency that yields a Redis client (`aioredis` for async) scoped to the request.
- Allow optional connection pooling and automatic reconnection on transient failures.
- Expose helper functions `cache_get(key)`, `cache_set(key, value, ttl=None)`.

## Verification Criteria
- [] Dependency `get_redis()` returns a connected `Redis` instance that can `PING` successfully.
- [] `cache_set` stores a value and `cache_get` retrieves the same value.
- [] Unit test `tests/dependencies/test_redis_dependency.py` spins up a temporary Redis container (via `testcontainers` or a mock) and validates set/get/expire.
- [] CI pipeline runs Redis‑dependency tests; if Redis not available, the test is skipped with a clear warning.

## Status
- [] Pending