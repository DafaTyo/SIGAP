# TASK‑BE‑006‑07 – Rate Limit Middleware (optional)

## Goals
- Throttle incoming requests per IP (or per authenticated `user_id`) to a configurable limit (default **100 req/min**).
- Return **429 Too Many Requests** when the limit is exceeded.
- Provide `Retry‑After` header indicating seconds until the next allowed request.
- Make the limit configurable via environment variables `RATE_LIMIT` and `RATE_WINDOW_SECONDS`.

## Verification Criteria
- [] After 100 requests within one minute from the same IP, the 101st request receives **429**.
- [] Header `Retry‑After` is present and reflects the remaining window seconds.
- [] Unit test `tests/middleware/test_rate_limit.py` simulates the request burst and asserts the 429 response and header.
- [] CI pipeline runs the rate‑limit tests and fails if the limit is not enforced.

## Status
- [] Pending