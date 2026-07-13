# TASK‑BE‑006‑01 – CORS Middleware

## Goals
- Enable Cross‑Origin Resource Sharing only for allowed origins defined in environment variable `ALLOWED_ORIGINS`.
- Reject any request with an origin not in the whitelist.
- Provide proper `Access‑Control‑Allow‑Credentials`, `Access‑Control‑Allow‑Headers`, and `Access‑Control‑Allow‑Methods` headers.

## Verification Criteria
- [] Header `Access‑Control‑Allow‑Origin` is present and matches one of the values in `ALLOWED_ORIGINS` for a valid request.
- [] Pre‑flight `OPTIONS` request returns `200` with correct `Access‑Control‑Allow‑Methods` and `Access‑Control‑Allow-Headers`.
- [] Requests from a disallowed origin receive `403` (or are blocked by the browser – we verify by checking the response missing the CORS headers).
- [] Unit test `tests/middleware/test_cors.py` asserts the above scenarios with FastAPI `TestClient`.
- [] CI pipeline runs the CORS test suite and fails if any criteria are not met.

## Status
- [] Pending