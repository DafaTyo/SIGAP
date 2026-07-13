# TASK‑BE‑006‑02 – GZip Middleware

## Goals
- Compress HTTP responses larger than 500 KB using gzip to reduce bandwidth.
- Preserve `Content‑Encoding` header correctly so clients can decompress.
- Ensure that streaming responses (e.g., large file download) are also compressed when appropriate.

## Verification Criteria
- [] Response payload > 500 KB includes header `Content‑Encoding: gzip`.
- [] Payload ≤ 500 KB is **not** compressed (no `Content‑Encoding` header).
- [] Unit test `tests/middleware/test_gzip.py` verifies both cases using FastAPI `TestClient` and a dummy endpoint that returns a large string.
- [] CI step runs the GZip test suite and fails on any regression.

## Status
- [] Pending