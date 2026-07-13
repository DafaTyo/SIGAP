# TASK‑BE‑006‑03 – Security Headers Middleware

## Goals
- Add security‑related HTTP headers to every response to mitigate common web attacks.
- Headers to include:
  - `X‑Content‑Type‑Options: nosniff`
  - `X‑Frame‑Options: DENY`
  - `Strict‑Transport‑Security: max-age=31536000; includeSubDomains; preload`
  - (optional) `Content‑Security‑Policy` according to project CSP policy.

## Verification Criteria
- [] Each response contains the three mandatory headers (`X‑Content‑Type‑Options`, `X‑Frame‑Options`, `Strict‑Transport‑Security`).
- [] CSP header is present when environment variable `ENABLE_CSP` is set to `1`.
- [] Unit test `tests/middleware/test_security_headers.py` validates presence of these headers for a sample endpoint.
- [] CI pipeline runs the security‑header tests and fails if any header is missing.

## Status
- [] Pending