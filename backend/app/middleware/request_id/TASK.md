# TASK‑BE‑006‑04 – Request ID Middleware

## Goals
- Generate a unique UUID4 for each incoming HTTP request.
- Store the ID in `request.state.request_id` for downstream access (logging, audit).
- Add the ID to the response header `X‑Request‑ID` so the client can correlate logs.
- Provide a helper function `get_request_id()` that can be imported anywhere in the codebase.

## Verification Criteria
- [] Every request receives a non‑empty `X‑Request‑ID` header.
- [] The same ID is available in `request.state.request_id` inside any endpoint handler.
- [] Unit test `tests/middleware/test_request_id.py` asserts that two consecutive requests have *different* IDs and that the ID can be fetched via `get_request_id()`.
- [] CI pipeline runs the Request‑ID tests and fails on mismatch.

## Status
- [] Pending